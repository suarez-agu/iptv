# IPTV-org El Trece mirror

This repository mirrors IPTV-org's country-grouped public playlist and replaces
its El Trece Argentina stream with the configured stream in `update.py`:

- Source playlist: <https://iptv-org.github.io/iptv/index.country.m3u>
- El Trece stream: <https://livetrx01.vodgc.net/eltrecetv/index.m3u8>
- Referrer sent by compatible players: <https://vodgc.net>

The GitHub Actions workflow runs every six hours and can also be started manually.
It writes the patched playlist to `docs/index.country.m3u` and commits changes to
the repository.

## First run

1. In this repository, open **Settings → Actions → General** and confirm that
   workflows are allowed to run. The workflow needs permission to write contents
   so it can commit the generated playlist. If the repository's Actions policy
   restricts write permissions, allow this workflow to write repository contents.
2. Push the initial files to GitHub so the repository has a branch and a default
   branch. Then open the **Actions** tab, choose **Update IPTV mirror**, and select
   **Run workflow** on that default branch.
3. Once the run succeeds, `docs/index.country.m3u` will appear in the repository.

The workflow runs the included unit tests before downloading and patching the
source playlist. It stops without publishing if it cannot identify exactly one
El Trece entry.

## Playlist access

This repository is private. Its raw GitHub URL requires authentication, so
unauthenticated clients cannot access it. After pushing the initial files and
creating a default branch, an authenticated client can use this URL, with
`<BRANCH>` replaced by the actual branch name:

```text
https://raw.githubusercontent.com/suarez-agu/iptv/<BRANCH>/docs/index.country.m3u
```

To make the playlist available to an unauthenticated app, GitHub Pages is an
option only if the account plan allows Pages for private repositories. Pages
output is publicly accessible by default, even when the source repository is
private. After enabling Pages under **Settings → Pages** with **Deploy from a
branch**, the playlist URL will be:

```text
https://suarez-agu.github.io/iptv/index.country.m3u
```

If the account plan does not allow Pages for this private repository, use a
separate public repository for the playlist, or intentionally make this
repository public after reviewing all of its contents.

## Change the El Trece stream

Edit `EL_TRECE_URL` or `EL_TRECE_REFERRER` near the top of `update.py`, then run
the workflow manually to refresh the playlist.

This repository publishes playlist text containing stream references. It does
not host or relay the video streams.
