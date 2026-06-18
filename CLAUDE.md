# TESTS

## Struktura folderów
Testy tworzymy w lustrzanym odbiciu folderu `app/` w folderze `tests/`. Dodajemy iteracyjnie — tylko to co aktualnie testujemy, bez tworzenia z góry pustych plików.

## Typy testów i zakresy

| Warstwa | Typ testu | Co sprawdzamy |
|---|---|---|
| Presentation | E2E (httpx) | Payload → URL → asercje na odpowiedź (status code + body) |
| Infrastructure | Integracyjne | Klient bazodanowy → asercje na dane wyciągnięte z bazy |
| Application | Unit (wyjątki) | Tylko raisowane wyjątki przy określonych warunkach / symulacji błędu |

## Fixtures

- Twórz jak najwięcej fixture i używaj ich bezwzględnie.
- URL, klient HTTP, dane testowe — wszystko jako fixture.
- Fixture powtarzające się w 2+ miejscach → natychmiast przenieść do conftest właściwej warstwy.
- Fixture współdzielone na wielu warstwach → globalny `tests/conftest.py`.
- Callable fixtures: definiuj jako klasy duck-typing dziedziczące po `Protocol`, albo z nową składnią `type ClassName = Callable[[...], ...]`.
- Funkcje pomocnicze zwracające gotowe obiekty z określonymi danymi (np. `make_service(...)`, `make_dto(...)`, `make_entity(...)`) traktuj od razu jako fixture — przenoś do conftest. Jeśli obiekt wymaga innych fixture'ów jako argumentów, zostaje fixture przyjmującym je z DI.

## Struktura conftest

```
tests/
  conftest.py                          # globalne fixture wspólne dla wszystkich warstw
  modules/
    cinema/
      presentation/
        conftest.py                    # fixture tylko dla testów prezentacji
      application/
        conftest.py                    # fixture tylko dla testów aplikacji
      infrastructure/
        conftest.py                    # fixture tylko dla testów infrastruktury
```

Domain — nie potrzebuje conftest.

## Konfiguracja testów

- Środowisko testowe korzysta z pliku `.env.test` (lokalna baza, `localhost:8000`; nie Docker `db:5432`).
- Załadowanie ustawień: `Settings(_env_file=".env.test")` — identyczny wzorzec jak w kodzie produkcyjnym (pydantic-settings). Nigdy nie używać `os.environ.setdefault` ani `load_dotenv` wprost.
- Globalne fixtures (engine, db_session, client) żyją w `tests/conftest.py`.
- `engine` — scope session (tworzy/dropi tabele raz na całą sesję testową).
- `db_session` — scope function (każdy test dostaje transakcję, rollback na koniec).
- `client` — nadpisuje `get_session` dependency na aktywną `db_session`, żeby HTTP i repo dzieliły tę samą transakcję. Przed każdym testem woła `test_redis_client.flushdb()` — izolacja Redis analogiczna do rollbacku bazy.

## Typowanie parametrów testów

**Wszystkie** parametry metod testowych i funkcji testowych muszą być otyptowane. Dotyczy to fixture'ów wszelkiego rodzaju — nie tylko repozytoriów.

Zasady:
- Repozytoria: interfejs, nie konkretna klasa — `IMovieRepository`, nie `MovieRepository`.
- Mocki: `AsyncMock` (lub inny typ mocka).
- URL-e: `str`.
- Payloady: `dict[str, str | int | float | None]` lub dokładniejszy typ jeśli znany.
- Tokeny JWT: `str`.
- Odpowiedzi/obiekty z fixture'ów tworzących zasoby: `dict` (lub bardziej szczegółowy jeśli znany).
- Klient HTTP: `AsyncClient`.

```python
# dobrze
async def test_foo(self, client: AsyncClient, movies_url: str, admin_token: str): ...
async def test_bar(self, repo: IMovieRepository): ...
async def test_baz(self, mock_repo: AsyncMock): ...

# źle — brak typów
async def test_foo(self, client, movies_url, admin_token): ...
# źle — konkretna klasa zamiast interfejsu
async def test_bar(self, repo: MovieRepository): ...
```

## Konwencja repo / serwis

Repozytorium jest **głupim magazynem** — nie podejmuje decyzji biznesowych:
- Jeśli zasób istnieje → zwraca go.
- Jeśli zasobu nie ma → zwraca `None`.
- Nigdy nie raisuje `AppError` ani wyjątków domenowych.

Serwis (warstwa aplikacyjna) **orkiestruje** i **podejmuje decyzje**:
- Otrzymuje `None` od repo → raisuje odpowiedni wyjątek (`XxxNotFoundError`, itp.).
- Sygnatura zwracanego typu w interfejsie repozytorium: `Entity | None`.

## Zasady pisania testów

1. **YAGNI** — zero dodawania na zapas. Tylko to co aktualne.
2. **Brak duplikatów fixture** — identyczna fixture w 2 miejscach jest błędem.
3. **Konwencje nazewnictwa** — ogólnopowszechne, czytelne. Klasy testowe i metody są ok.
4. **Nie testuj oczywistości** — jeśli test A potwierdził że dane zniknęły, nie dodawaj testu B sprawdzającego że nie można ich pobrać po raz drugi.
5. **Sprawdzaj tylko ważne rzeczy** — asercje na kod HTTP i kluczowe pola body; nie sprawdzaj każdego pola jeśli nie wnosi wartości.

## Edge cases — symulacja realnego kina

Testy mają symulować flow kilku użytkowników naraz. Obowiązkowe scenariusze:

- Dwóch userów próbuje zarezerwować te same miejsca jednocześnie — jeden dostaje błąd.
- Próba rezerwacji miejsc już zajętych.
- Próba anulowania rezerwacji po rozpoczęciu seansu — błąd.
- Próba rezerwacji na seans który już się zakończył lub się odbywa.
- Wyczerpanie limitu miejsc w sali.

Jeśli przy pisaniu testu wykryty zostanie brakujący edge case (np. niezaimplementowana logika), **zatrzymać się i poinformować użytkownika** — nie implementować bez decyzji.

## Postęp implementacji

Testy implementujemy po kolei. Po każdej sesji odnotowujemy gdzie skończyliśmy, żeby móc kontynuować bez cofania się.

**Status:** Ukończone.

### Ukończone
- `tests/modules/auth/presentation/test_auth_router.py` — E2E (10 testów)
- `tests/modules/auth/infrastructure/test_auth_repository.py` — integracyjne (4 testy)
- `tests/modules/auth/application/test_auth_service.py` — wyjątki (7 testów)
- `tests/modules/cinema/presentation/test_movies_router.py` — E2E (10 testów)
- `tests/modules/cinema/presentation/test_halls_router.py` — E2E (5 testów)
- `tests/modules/cinema/presentation/test_screenings_router.py` — E2E (15 testów)
- `tests/modules/cinema/presentation/test_reservations_router.py` — E2E (10 testów)
- `tests/modules/cinema/infrastructure/test_movie_repository.py` — integracyjne (5 testów)
- `tests/modules/cinema/infrastructure/test_hall_repository.py` — integracyjne (4 testy)
- `tests/modules/cinema/infrastructure/test_screening_repository.py` — integracyjne (6 testów)
- `tests/modules/cinema/infrastructure/test_reservation_repository.py` — integracyjne (4 testy)
- `tests/modules/cinema/application/test_movie_service.py` — wyjątki (5 testów)
- `tests/modules/cinema/application/test_hall_service.py` — wyjątki (3 testy)
- `tests/modules/cinema/application/test_screening_service.py` — wyjątki (7 testów)
- `tests/modules/cinema/application/test_reservation_service.py` — wyjątki (6 testów)

---

# PROJECT STRUCTURE

Struktura zachowana tutaj dla szybkiej nawigacji — nazwy folderów i plików literalnie opisują zawartość.

```
app/
├── main.py                              # punkt wejścia FastAPI, rejestracja routerów
├── modules/
│   ├── auth/                            # bounded context: uwierzytelnianie i użytkownicy
│   │   ├── application/
│   │   │   ├── dto/
│   │   │   │   ├── login_dto.py
│   │   │   │   └── register_user_dto.py
│   │   │   ├── exceptions/
│   │   │   │   ├── different_passwords_error.py
│   │   │   │   ├── duplicate_email_error.py
│   │   │   │   ├── refresh_token_expire_error.py
│   │   │   │   ├── refresh_token_not_found_error.py
│   │   │   │   └── wrong_password_error.py
│   │   │   ├── interface/
│   │   │   │   └── i_auth_service.py
│   │   │   └── service/
│   │   │       └── auth_service.py
│   │   ├── domain/
│   │   │   └── entities/
│   │   │       ├── refresh_token.py
│   │   │       └── user.py
│   │   ├── infrastructure/
│   │   │   ├── interface/
│   │   │   │   └── i_auth_repository.py
│   │   │   ├── orm/
│   │   │   │   ├── refresh_token_orm.py
│   │   │   │   └── user_orm.py
│   │   │   └── repository/
│   │   │       └── auth_repository.py
│   │   └── presentation/
│   │       ├── dependencies/
│   │       │   └── auth_deps.py         # Depends() dla endpointów auth
│   │       ├── routers/v1/
│   │       │   └── auth_router.py
│   │       └── schemas/
│   │           ├── requests/
│   │           │   ├── login_request.py
│   │           │   ├── logout_request.py
│   │           │   ├── refresh_request.py
│   │           │   └── register_request.py
│   │           └── responses/
│   │               ├── login_response.py
│   │               ├── refresh_response.py
│   │               ├── register_user_response.py
│   │               └── tokens_response.py
│   │
│   ├── cinema/                          # bounded context: filmy, sale, seanse, rezerwacje
│   │   ├── application/
│   │   │   ├── dto/
│   │   │   │   ├── add_hall_dto.py
│   │   │   │   ├── add_movie_dto.py
│   │   │   │   ├── add_screening_dto.py
│   │   │   │   ├── create_reservation_dto.py
│   │   │   │   ├── reservation_dto.py          # ReservationDTO + nested (ScreeningDTO, MovieDTO, HallDTO)
│   │   │   │   ├── reservation_hold_dto.py     # HoldDTO, ReservationHoldDTO, SeatHoldData
│   │   │   │   ├── screening_details_dto.py    # ScreeningDetailsDTO, MovieData, SeatData
│   │   │   │   └── update_screening_dto.py
│   │   │   ├── excpetions/              # [typo w folderze — tak jest w repo]
│   │   │   │   ├── hall_not_found_error.py
│   │   │   │   ├── movie_not_found_error.py
│   │   │   │   ├── permission_denied_error.py
│   │   │   │   ├── reservation_cancellation_error.py
│   │   │   │   ├── reservation_data_not_found_error.py
│   │   │   │   ├── reservation_mismatch_error.py
│   │   │   │   ├── reservation_not_found_error.py
│   │   │   │   ├── screening_not_available_error.py
│   │   │   │   ├── screening_not_found_error.py
│   │   │   │   └── seat_unavailable_error.py
│   │   │   ├── interface/
│   │   │   │   ├── i_hall_service.py
│   │   │   │   ├── i_movie_service.py
│   │   │   │   ├── i_reservation_service.py
│   │   │   │   └── i_screening_service.py
│   │   │   └── service/
│   │   │       ├── hall_service.py
│   │   │       ├── movie_service.py
│   │   │       ├── reservation_service.py
│   │   │       └── screening_service.py
│   │   ├── domain/
│   │   │   └── entities/
│   │   │       ├── hall.py
│   │   │       ├── movie.py
│   │   │       ├── reservation.py
│   │   │       ├── screening.py
│   │   │       ├── screening_seat.py
│   │   │       └── seat.py
│   │   ├── infrastructure/
│   │   │   ├── interface/
│   │   │   │   ├── i_hall_repository.py
│   │   │   │   ├── i_movie_repository.py
│   │   │   │   ├── i_reservation_hold_repository.py
│   │   │   │   ├── i_reservation_repository.py
│   │   │   │   ├── i_screening_repository.py
│   │   │   │   └── i_screening_seat_repository.py
│   │   │   ├── mappers/
│   │   │   │   ├── hall_mapper.py
│   │   │   │   ├── movie_mapper.py
│   │   │   │   ├── reservation_mapper.py
│   │   │   │   ├── screening_mapper.py
│   │   │   │   ├── screening_seat_mapper.py
│   │   │   │   └── seat_mapper.py
│   │   │   ├── orm/
│   │   │   │   ├── hall_orm.py
│   │   │   │   ├── movie_orm.py
│   │   │   │   ├── reservation_orm.py
│   │   │   │   ├── reserved_seat_orm.py
│   │   │   │   ├── screening_orm.py
│   │   │   │   ├── screening_seat_orm.py
│   │   │   │   └── seat_orm.py
│   │   │   └── repository/
│   │   │       ├── hall_repository.py
│   │   │       ├── movie_repository.py
│   │   │       ├── reservation_hold_repository.py  # Redis — hold seats
│   │   │       ├── reservation_repository.py
│   │   │       ├── screening_repository.py
│   │   │       └── screening_seat_repository.py
│   │   └── presentation/
│   │       ├── dependencies/
│   │       │   ├── hall_deps.py
│   │       │   ├── movie_deps.py
│   │       │   ├── reservation_deps.py
│   │       │   └── screening_deps.py
│   │       ├── routers/v1/
│   │       │   ├── halls_router.py
│   │       │   ├── movies_router.py
│   │       │   ├── reservation_router.py
│   │       │   └── screenings_router.py
│   │       └── schemas/
│   │           ├── request/
│   │           │   ├── add_hall_request.py
│   │           │   ├── add_movie_request.py
│   │           │   ├── add_screening_request.py
│   │           │   ├── create_reservation_request.py
│   │           │   ├── hold_seats_request.py
│   │           │   └── update_screening_request.py
│   │           └── responses/
│   │               ├── add_hall_response.py         # AddHallResponse(hall_id)
│   │               ├── add_movie_response.py        # AddMovieResponse(movie_id)
│   │               ├── add_screening_response.py    # AddScreeningResponse(screening_ids)
│   │               ├── hold_seats_response.py       # HoldSeatsResponse, SeatHoldResponse
│   │               ├── movie_detail_response.py     # MovieDetailResponse
│   │               ├── movie_list_response.py       # MovieListResponse(items, total, page, limit)
│   │               ├── reservation_history_response.py  # ReservationHistoryResponse(reservations, total, page, limit)
│   │               ├── reservation_response.py      # ReservationResponse + nested (Screening, Movie, Hall, Seat)
│   │               └── screening_detail_response.py # ScreeningDetailResponse + nested (Movie, Seat)
│   │
│   ├── healthcheck/
│   │   └── healthcheck.py
│   │
│   └── shared/
│       ├── config/
│       │   └── settings.py              # zmienne środowiskowe (pydantic Settings)
│       ├── database_conn/
│       │   ├── base_orm.py              # deklaratywna baza SQLAlchemy
│       │   ├── database_client.py       # async session factory
│       │   └── redis_client.py          # async Redis client
│       ├── dependencies/
│       │   └── auth_deps.py             # get_current_user — wspólny dla wszystkich modułów
│       └── exceptions/
│           ├── app_error.py
│           ├── expired_token_error.py
│           ├── invalid_data_error.py
│           └── invalid_token_error.py
│
├── docker-compose.yaml
├── Dockerfile
└── CLAUDE.md
```
