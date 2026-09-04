create table public.anon_messages (
  id bigint generated always as identity primary key,
  sender_telegram_id bigint not null,
  target_telegram_id bigint not null,
  body text not null,
  created_at timestamptz not null default now()
);

create index anon_messages_sender_created_idx
  on public.anon_messages (sender_telegram_id, created_at);

alter table public.anon_messages enable row level security;

create table public.anon_blocks (
  blocker_telegram_id bigint not null,
  blocked_telegram_id bigint not null,
  created_at timestamptz not null default now(),
  primary key (blocker_telegram_id, blocked_telegram_id)
);

alter table public.anon_blocks enable row level security;
