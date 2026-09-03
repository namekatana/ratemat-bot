update public.profile_ratings set score = 5 where score > 5;

alter table public.profile_ratings drop constraint profile_ratings_score_check;
alter table public.profile_ratings add constraint profile_ratings_score_check
  check (score between 1 and 5);
