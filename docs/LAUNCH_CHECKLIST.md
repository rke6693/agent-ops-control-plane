# Launch Checklist

Use this checklist before making the repo public or posting launch content.

## Repo

- [ ] `python -m unittest discover -s tests` passes.
- [ ] `agent-ops scan README.md docs examples src tests assets` passes.
- [ ] `.env` is not tracked.
- [ ] `.venv/` is not tracked.
- [ ] Generated private artifacts are not tracked.
- [ ] README has install, status, scan, test, and launch-queue commands.
- [ ] GitHub Actions CI is enabled.
- [ ] Issues are enabled.

## Assets

- [ ] README hero image generated or prompt pack committed.
- [ ] Architecture image generated or prompt pack committed.
- [ ] X card image generated or prompt pack committed.
- [ ] Asset filenames and alt text reviewed.
- [ ] No generated image contains readable fake secrets or private data.

## Social

- [ ] X launch thread reviewed manually.
- [ ] Repo URL inserted.
- [ ] Launch queue generated.
- [ ] Launch queue secret scan passes.
- [ ] `approval_required` is true for every queued post.
- [ ] `live_publish_enabled` is false unless a reviewed adapter is present.

## External Actions

- [ ] Public GitHub repo creation explicitly approved.
- [ ] First push explicitly approved.
- [ ] Live X posting explicitly approved separately.
- [ ] If posting via API, exact typed confirmation is captured and audited.

