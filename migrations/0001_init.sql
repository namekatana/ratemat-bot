create table public.users (
  id bigint generated always as identity primary key,
  telegram_id bigint unique not null,
  username text,
  first_name text,
  last_name text,
  verification_status text not null default 'pending_start',
  verification_file_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.users add constraint users_verification_status_check
  check (verification_status in ('pending_start', 'awaiting_video', 'pending_review', 'verified', 'rejected'));

create index users_verification_status_idx on public.users (verification_status);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger users_set_updated_at
  before update on public.users
  for each row
  execute function public.set_updated_at();

alter table public.users enable row level security;
