create table public.profiles (
  id bigint generated always as identity primary key,
  telegram_id bigint unique not null references public.users(telegram_id) on delete cascade,
  name text not null,
  age smallint not null,
  gender text not null,
  photo_file_id text not null,
  description text not null,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.profiles add constraint profiles_gender_check check (gender in ('male', 'female'));
alter table public.profiles add constraint profiles_age_check check (age between 18 and 99);
alter table public.profiles add constraint profiles_name_len_check check (char_length(name) between 2 and 32);
alter table public.profiles add constraint profiles_description_len_check check (char_length(description) between 10 and 500);
create trigger profiles_set_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();
alter table public.profiles enable row level security;

create table public.profile_ratings (
  id bigint generated always as identity primary key,
  rater_telegram_id bigint not null,
  target_telegram_id bigint not null,
  score smallint not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (rater_telegram_id, target_telegram_id)
);
alter table public.profile_ratings add constraint profile_ratings_score_check check (score between 1 and 10);
create index profile_ratings_rater_idx on public.profile_ratings (rater_telegram_id);
create index profile_ratings_target_idx on public.profile_ratings (target_telegram_id);
create trigger profile_ratings_set_updated_at
  before update on public.profile_ratings
  for each row execute function public.set_updated_at();
alter table public.profile_ratings enable row level security;
