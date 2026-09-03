create table public.admins (
  id bigint generated always as identity primary key,
  telegram_id bigint unique not null,
  note text,
  created_at timestamptz not null default now()
);
alter table public.admins enable row level security;

create table public.complaints (
  id bigint generated always as identity primary key,
  reporter_telegram_id bigint not null,
  target_telegram_id bigint,
  target_username text,
  reason text not null,
  status text not null default 'open',
  created_at timestamptz not null default now(),
  resolved_at timestamptz,
  resolved_by bigint
);
alter table public.complaints add constraint complaints_status_check
  check (status in ('open', 'resolved_ban', 'resolved_dismiss'));
create index complaints_status_idx on public.complaints (status);
alter table public.complaints enable row level security;

alter table public.users drop constraint users_verification_status_check;
alter table public.users add constraint users_verification_status_check
  check (verification_status in ('pending_start', 'awaiting_video', 'pending_review', 'verified', 'rejected', 'banned'));
