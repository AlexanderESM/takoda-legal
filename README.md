# Takoda Digital legal website

A static, British English legal website for The Art of Dining. No external fonts, JavaScript, trackers, advertising scripts, login or PDF reader is needed.

## Current status

Prepared locally; **not published**. GitHub CLI was not installed in the preparation environment, so no authenticated GitHub username, repository URL or public Pages URL could be established. `deployment-status.json` records this explicitly. Do not paste a guessed address into Google Play or the Android app.

Files:
- `index.html`: Takoda Digital legal landing page.
- `privacy.html`: the complete 15-section Privacy Policy.
- `assets/style.css`: shared responsive styles.
- `.nojekyll`: publish the static files without Jekyll processing.
- `REVIEW.md`: implementation evidence and unresolved release/compliance work.
- `scripts/validate_site.py`: offline HTML/link/content/security checks.
- `scripts/prepare_publication.py`: update the effective date on the actual publication day.
- `scripts/record_deployment.py`: verify the real unauthenticated HTTPS page and record its URL.

## Local preview and checks

From this folder, using Python 3. The commands below prefer the existing bundled Python runtime on the preparation machine and otherwise use an installed Python. You may set `$python` to any working Python 3 executable:

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $python)) { $python = (Get-Command python -ErrorAction Stop).Source }
& $python scripts/validate_site.py
& $python -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/index.html` or `http://127.0.0.1:8767/privacy.html`. A local preview is not a Google Play policy URL.

## Publish a new repository to GitHub Pages

The following commands are for Windows PowerShell. Run them from this website repository, not the Android project and not its parent folder. Publish only these static-site files; never copy upload keys, password files, AABs or Android project files into this repository.

1. Install GitHub CLI if needed, restart the terminal, and sign in using its browser flow:

```powershell
winget install --id GitHub.cli --exact
# Open a new PowerShell window after installation.
gh auth login --hostname github.com --git-protocol https --web
gh auth status
gh auth setup-git
```

2. Determine the account from authentication, then check the intended repository:

```powershell
$login = gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($login)) { throw 'GitHub authentication is required.' }
$repository = "$login/takoda-legal"
gh repo view $repository --json nameWithOwner,url,visibility,defaultBranchRef
```

If the repository exists, **stop here and follow the existing-repository procedure below**. Only proceed with creation after confirming that the view failure is genuinely `Not Found`; an authentication, permission or network failure is not evidence that the repository is absent.

3. Set the publication date, validate, commit and publish. A local `main` Git repository and initial commit are already provided. If using a ZIP copy without `.git`, initialise it with `git init -b main` first.

```powershell
$python = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $python)) { $python = (Get-Command python -ErrorAction Stop).Source }
& $python scripts/prepare_publication.py
& $python scripts/validate_site.py
if ($LASTEXITCODE -ne 0) { throw 'Site validation failed.' }
git status --short
git add index.html privacy.html assets .nojekyll README.md REVIEW.md deployment-status.json scripts .gitignore
git diff --cached --check
git diff --cached --quiet
if ($LASTEXITCODE -eq 1) { git commit -m 'Prepare legal site for publication' }
gh repo create $repository --public --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'Repository publication failed. Do not continue.' }
```

4. Configure Pages to deploy from `main` and `/` (the repository root). The JSON is written outside the repository and contains no secret:

```powershell
$pagesConfig = Join-Path $env:TEMP 'takoda-pages-source.json'
'{"source":{"branch":"main","path":"/"}}' | Set-Content -LiteralPath $pagesConfig -Encoding ascii
gh api --method POST "repos/$repository/pages" --input $pagesConfig
```

If Pages already exists, inspect it with `gh api "repos/$repository/pages"`; update its source with `--method PUT` only if needed. Alternatively use **Repository Settings > Pages > Build and deployment > Deploy from a branch > main > /(root) > Save**. Do not enable access restrictions. Retain GitHub's HTTPS URL and enable Enforce HTTPS when available.

5. Retrieve the actual address and wait for a successful Pages build:

```powershell
gh api "repos/$repository/pages" --jq '{status: .status, html_url: .html_url, source: .source, https_enforced: .https_enforced}'
gh api "repos/$repository/pages/builds/latest" --jq '{status: .status, error: .error.message}'
$site = gh api "repos/$repository/pages" --jq .html_url
$policyUrl = $site.TrimEnd('/') + '/privacy.html'
& $python scripts/record_deployment.py --url $policyUrl --repository $repository
if ($LASTEXITCODE -ne 0) { throw 'Live verification failed. Do not use the URL yet.' }
Write-Output "Google Play Console > Privacy policy: $policyUrl"
```

Open that exact address in a private browser window without signing in. Check it from another network where possible. A single HTTP check verifies neither universal geographic accessibility nor legal compliance. Fix any HTTP error, login redirect, TLS problem or geographical restriction before using the page.

After successful verification, record the deployed status:

```powershell
git add deployment-status.json
git commit -m 'Record verified public policy URL'
git push origin main
```

## If takoda-legal already exists

Inspect and clone it rather than overwriting it:

```powershell
gh repo view $repository --json url,defaultBranchRef,visibility
gh api "repos/$repository/contents" --jq '.[].name'
gh repo clone $repository ../takoda-legal-existing
git -C ../takoda-legal-existing status --short
git -C ../takoda-legal-existing log -5 --oneline
```

Review its README, legal pages, Pages configuration and default branch. Preserve existing policies and unrelated files. If `privacy.html` already concerns a different app, do not replace it: choose a distinct page name and update the new site's links and actual final URL. If `assets/style.css` is shared by other pages, use a new stylesheet name and update only the new pages.

Copy only reviewed files into the clone. Review `git diff`, run the site checks there, commit to `main` only when appropriate for the existing repository, and push normally. Never force-push. Configure Pages from `main` and `/` only after checking that this will not break its existing deployment. Obtain and verify the real URL using step 5 above.

## Android entry and Google Play

The inspected Android settings screen has no policy link. No Android source was modified during local preparation because there is not yet a verified public URL. After the page is published and verified, add a **Privacy Policy** entry in Settings pointing to that exact URL; increment the Android version/code, add an intent/navigation test, and run the required build and device checks before creating a replacement signed AAB. Do not represent version 1.1.0/code 25 as already containing the entry.

Use the same verified `privacy.html` URL in **Google Play Console > App content > Privacy policy**. The policy does not replace the Data safety form, consent implementation or other release checks in REVIEW.md.

## Maintenance

Check the actual SDKs, permissions, consent flow and data handling before changing the policy. Preserve the 15-section structure and accurate app/developer details. Run `prepare_publication.py` before publishing a revised policy so its effective date matches publication, validate the files, review the diff, commit, push and re-verify HTTPS. Keep the page publicly accessible while the app is offered. No legal guarantee is implied by these technical checks.
