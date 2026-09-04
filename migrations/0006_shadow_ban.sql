alter table public.complaints add column kind text not null default 'user';
alter table public.complaints add constraint complaints_kind_check
  check (kind in ('user', 'auto_shadow'));

alter table public.users add column shadow_banned_at timestamptz;

create index complaints_target_created_idx
  on public.complaints (target_telegram_id, created_at);
