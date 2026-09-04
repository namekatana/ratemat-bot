alter table public.users add column premium_until timestamptz;

create table public.star_payments (
  id bigint generated always as identity primary key,
  telegram_id bigint not null,
  charge_id text unique not null,
  stars integer not null,
  payload text,
  created_at timestamptz not null default now()
);
create index star_payments_telegram_id_idx on public.star_payments (telegram_id);
alter table public.star_payments enable row level security;
