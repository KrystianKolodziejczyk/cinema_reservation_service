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

**Status:** W toku.

### Ukończone
- `tests/modules/auth/presentation/test_auth_router.py` — E2E (10 testów)
- `tests/modules/auth/infrastructure/test_auth_repository.py` — integracyjne (4 testy)
- `tests/modules/auth/application/test_auth_service.py` — wyjątki (7 testów)

### Następne
- `tests/modules/cinema/` — bounded context cinema (movies, halls, screenings, reservations)

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
