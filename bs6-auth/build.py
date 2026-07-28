#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Auth Pages pack: an index gallery plus one page per variant.

Every variant shares the same chrome (sticky bar with a back link and a colour-mode
toggle) so the pack reads as one product, while each form body is genuinely
different. Eight sign-in surfaces, covering the whole account journey from login to
lockout — including the two v6 components that make it possible without a plugin.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Auth Pages"
ROOT = pathlib.Path(__file__).parent

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{p}assets/vendor/bootstrap6/css/bootstrap.min.css">
<link rel="stylesheet" href="{p}assets/css/base.css">
<link rel="stylesheet" href="{p}assets/css/style.css">
</head>
<body>
"""

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

CARET = ('<svg class="combobox-caret" width="10" height="16" viewBox="0 0 10 16" fill="none" '
         'xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M0.46967 5.46967C0.762563 5.17678 '
         '1.23744 5.17678 1.53033 5.46967L5 8.93934L8.46967 5.46967C8.76256 5.17678 9.23744 5.17678 9.53033 '
         '5.46967C9.82322 5.76256 9.82322 6.23744 9.53033 6.53033L5.53033 10.5303C5.23744 10.8232 4.76256 '
         '10.8232 4.46967 10.5303L0.46967 6.53033C0.176777 6.23744 0.176777 5.76256 0.46967 5.46967Z" '
         'fill="currentcolor"/></svg>')

MAIL = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
        'aria-hidden="true"><rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="m2 4 6 4.5L14 4"/></svg>')

SEARCH = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
          'aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 4 4" stroke-linecap="round"/></svg>')

ACC_ICON = ('<svg class="accordion-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" '
            'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m2 5 6 6 6-6"/></svg>')


def combobox(name, placeholder, options, search=False, multiple=False):
    attrs = 'data-bs-toggle="combobox"'
    if search:
        attrs += ' data-bs-search="true"'
    if multiple:
        attrs += ' data-bs-multiple="true"'
    items = "\n      ".join(
        f'<button class="menu-item" type="button" data-bs-value="{v}">{l}</button>' for v, l in options)
    return f"""<button class="form-control combobox-toggle" type="button" {attrs} data-bs-name="{name}" data-bs-placeholder="{placeholder}">
      <span class="combobox-value">{placeholder}</span>
      {CARET}
    </button>
    <div class="menu">
      {items}
    </div>"""


# (folder, nav title, card title, blurb, sketch, wide?, form html)
VARIANTS = [
    ("01-signin", "Sign in", "Classic sign in",
     "Email and password on a centred card, with an adorned input and native :user-invalid feedback.",
     '<i class="w40"></i><i class="tall"></i><i class="w40"></i><i class="tall"></i><div class="row2"><i class="w40"></i><i class="w40"></i></div><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Welcome back</h1>
  <p class="fg-2 mb-5">Sign in to pick up where you left off.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="a1email">Email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="a1email" autocomplete="email" required>
      </div>
      <div class="invalid-feedback">Enter the email you signed up with.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="a1pw">Password</label>
      <input type="password" class="form-control" id="a1pw" autocomplete="current-password" required>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
      <div class="form-field mb-0">
        <input type="checkbox" class="check" id="a1keep" checked>
        <label for="a1keep">Keep me signed in</label>
      </div>
      <a class="fs-sm" href="../03-forgot/index.html">Forgot password?</a>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Signed in &#10003;">Sign in</button></div>
    <p class="fs-sm fg-3 text-center mb-0">New here? <a href="../02-register/index.html">Create an account</a></p>
  </form>
</div>"""),

    ("02-register", "Register", "Register with strength",
     "Account creation using the new password Strength meter, which fills as the password improves.",
     '<i class="w40"></i><i class="tall"></i><i class="w40"></i><i class="tall"></i><div class="row2"><i></i><i></i><i></i><i></i></div><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Create your account</h1>
  <p class="fg-2 mb-5">Free for 14 days. No card needed.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="a2name">Full name</label>
      <input type="text" class="form-control" id="a2name" autocomplete="name" required>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="a2email">Work email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="a2email" autocomplete="email" required>
      </div>
    </div>
    <div class="form-field">
      <label class="form-label" for="a2pw">Password</label>
      <input type="password" class="form-control" id="a2pw" autocomplete="new-password" required>
      <div class="strength" data-bs-strength>
        <div class="strength-segment"></div><div class="strength-segment"></div>
        <div class="strength-segment"></div><div class="strength-segment"></div>
      </div>
      <div class="form-text">Twelve characters or more, and please don&#8217;t reuse one.</div>
    </div>
    <div class="form-field">
      <input type="checkbox" class="check" id="a2terms" required>
      <label for="a2terms">I accept the terms of service</label>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Account created &#10003;">Create account</button></div>
  </form>
</div>"""),

    ("03-forgot", "Forgot", "Forgot password",
     "A single field and an honest message — deliberately vague about whether the address exists.",
     '<i class="w60" style="margin-inline:auto"></i><i class="tall"></i><i class="cta" style="margin-inline:auto"></i>',
     False, """<div class="form-shell text-center">
  <span class="icon-tile mx-auto mb-4">""" + MAIL + """</span>
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Reset your password</h1>
  <p class="fg-2 mb-5">Enter your email and we&#8217;ll send a reset link. It expires in an hour.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field text-start">
      <label class="form-label" for="a3email">Email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="a3email" autocomplete="email" required>
      </div>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Link sent &#10003;">Send reset link</button></div>
    <p class="fs-sm fg-3 mb-0"><a href="../01-signin/index.html">&#8592; Back to sign in</a></p>
  </form>
</div>"""),

    ("04-reset", "Reset", "Set a new password",
     "The other half of the reset flow, with the Strength meter and a confirmation field.",
     '<i class="w60" style="margin-inline:auto"></i><i class="tall"></i><div class="row2"><i></i><i></i><i></i><i></i></div><i class="tall"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Choose a new password</h1>
  <p class="fg-2 mb-5">Signing in on every device will be required again afterwards.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="a4pw">New password</label>
      <input type="password" class="form-control" id="a4pw" autocomplete="new-password" required>
      <div class="strength" data-bs-strength>
        <div class="strength-segment"></div><div class="strength-segment"></div>
        <div class="strength-segment"></div><div class="strength-segment"></div>
      </div>
    </div>
    <div class="form-field">
      <label class="form-label" for="a4pw2">Confirm password</label>
      <input type="password" class="form-control" id="a4pw2" autocomplete="new-password" required>
      <div class="invalid-feedback">Both passwords need to match.</div>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Password changed &#10003;">Set new password</button></div>
  </form>
</div>"""),

    ("05-twofactor", "2FA", "Two-factor verification",
     "The OTP input handling a six-digit code, with paste support and one-time-code autofill.",
     '<i class="w60" style="margin-inline:auto"></i><div class="row2"><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i></div><i class="cta" style="margin-inline:auto"></i>',
     False, """<div class="form-shell text-center">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Two-step verification</h1>
  <p class="fg-2 mb-5">Enter the six-digit code from your authenticator app.</p>
  <form class="vstack gap-4" data-demo-form novalidate>
    <div>
      <label class="form-label visually-hidden" for="a5otp">Verification code</label>
      <div class="otp d-inline-flex" data-bs-otp>
        <input type="text" class="otp-input" maxlength="6" id="a5otp" aria-label="Verification code" autocomplete="one-time-code">
      </div>
    </div>
    <div class="form-field justify-content-center">
      <input type="checkbox" class="check" id="a5trust">
      <label for="a5trust">Trust this device for 30 days</label>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Verified &#10003;">Verify</button></div>
    <p class="fs-sm fg-3 mb-0">Lost your device? <a href="#">Use a recovery code</a></p>
  </form>
</div>"""),

    ("06-magic", "Magic link", "Passwordless sign in",
     "Email-only sign in, with the sent state shown inline rather than on a separate page.",
     '<i class="w60" style="margin-inline:auto"></i><i class="tall"></i><i class="cta"></i><i class="w75" style="margin-inline:auto"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sign in without a password</h1>
  <p class="fg-2 mb-5">We&#8217;ll email you a link that signs you straight in.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="a6email">Email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="a6email" autocomplete="email" required>
      </div>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Link sent &#10003;">Email me a link</button></div>
  </form>
  <div class="alert theme-info mt-4 mb-0" role="alert">
    <strong>Already requested one?</strong> Links last 15 minutes and only work once.
  </div>
  <hr class="my-4">
  <p class="fs-sm fg-3 text-center mb-0">Prefer a password? <a href="../01-signin/index.html">Sign in normally</a></p>
</div>"""),

    ("07-sso", "SSO", "SSO and social sign in",
     "Provider buttons above a divider, with a workspace Combobox for organisations on SAML.",
     '<div class="row2"><i class="tall"></i><i class="tall"></i></div><i class="w40" style="margin-inline:auto"></i><i class="tall"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sign in to your workspace</h1>
  <p class="fg-2 mb-5">Use your company account, or pick a provider.</p>
  <div class="vstack gap-2 mb-4">
    <button class="btn-outline theme-secondary w-100" type="button">Continue with Google</button>
    <button class="btn-outline theme-secondary w-100" type="button">Continue with Microsoft</button>
    <button class="btn-outline theme-secondary w-100" type="button">Continue with GitHub</button>
  </div>
  <div class="d-flex align-items-center gap-3 mb-4">
    <hr class="flex-grow-1 my-0"><span class="fs-xs fg-3">OR SAML SSO</span><hr class="flex-grow-1 my-0">
  </div>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div>
      <label class="form-label">Workspace</label>
      """ + combobox("workspace", "Find your workspace…", [("a","northwind.app"),("b","kestrel.io"),("c","lumen.co")], search=True) + """
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Redirecting &#10003;">Continue with SSO</button></div>
  </form>
</div>"""),

    ("08-lock", "Lock screen", "Locked session",
     "The return-from-idle screen: identity already known, so only the password is asked for.",
     '<i class="tall" style="min-height:3rem;width:3rem;border-radius:99px;margin-inline:auto"></i><i class="w40" style="margin-inline:auto"></i><i class="tall"></i><i class="cta"></i>',
     False, """<div class="form-shell text-center">
  <span class="avatar avatar-lg mx-auto mb-3"><span class="avatar-initials">PN</span></span>
  <h1 class="fs-xl fw-semibold mb-1">Priya Nadkarni</h1>
  <p class="fg-3 fs-sm mb-5">Locked after 15 minutes idle</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field text-start">
      <label class="form-label" for="a8pw">Password</label>
      <input type="password" class="form-control" id="a8pw" autocomplete="current-password" required>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Unlocked &#10003;">Unlock</button></div>
    <p class="fs-sm fg-3 mb-0"><a href="../01-signin/index.html">Sign in as someone else</a></p>
  </form>
</div>"""),
]


def write_variant(i, folder, nav, card, blurb, sketch, wide, body):
    prev_i = (i - 1) % len(VARIANTS)
    next_i = (i + 1) % len(VARIANTS)
    html = HEAD.format(
        title=f"{card} — {PACK_TITLE}",
        desc=f"{blurb} A free Bootstrap 6 form example.",
        p="../")
    html += f"""
<div class="variant-bar">
  <a class="btn-text btn-sm" href="../index.html">&#8592; All forms</a>
  <span class="fs-sm fw-semibold ms-2">{card}</span>
  <span class="fs-xs fg-3 d-none md:d-inline">{i + 1} of {len(VARIANTS)}</span>
  <div class="d-flex align-items-center gap-2 ms-auto">
    <a class="btn-icon btn-sm" href="../{VARIANTS[prev_i][0]}/index.html" aria-label="Previous form">&#8249;</a>
    <a class="btn-icon btn-sm" href="../{VARIANTS[next_i][0]}/index.html" aria-label="Next form">&#8250;</a>
    {TOGGLE}
  </div>
</div>

<main class="variant-stage">
  <div class="variant-inner{' is-wide' if wide else ''}">
    {body}
  </div>
</main>

<script type="module" src="../assets/js/main.js"></script>
</body>
</html>
"""
    d = ROOT / folder
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_index():
    cards = []
    for i, (folder, nav, card, blurb, sketch, wide, body) in enumerate(VARIANTS, 1):
        cards.append(f"""      <a class="pack-card" href="{folder}/index.html">
        <div class="pack-thumb"><div class="sketch">{sketch}</div></div>
        <div class="pack-card-body">
          <p class="fs-xs fg-3 mb-1">{i:02d}</p>
          <h2 class="pack-card-title">{card}</h2>
          <p class="fg-2 fs-sm mb-0">{blurb}</p>
        </div>
      </a>""")

    html = HEAD.format(
        title=f"{PACK_TITLE} — 10 Free Bootstrap 6 Form Templates",
        desc="Ten free Bootstrap 6 form templates — contact, sign-up, booking, multi-step, OTP verification, chips, range and floating labels. No build step.",
        p="")
    html += f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#forms">Skip to the forms</a>

<div class="pack-head">
  <div class="container">
    <div class="d-flex flex-wrap align-items-start gap-3">
      <div class="me-auto" style="max-width:44rem">
        <span class="badge badge-subtle theme-primary mb-3">Bootstrap 6.0.0-alpha1</span>
        <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">{PACK_TITLE}</h1>
        <p class="fs-lg fg-2 mb-0">
          Ten form layouts covering the shapes real projects need &#8212; contact,
          sign-up, booking, multi-step, verification and filtering. Between them they
          use every form component Bootstrap 6 added over v5.
        </p>
      </div>
      {TOGGLE}
    </div>
  </div>
</div>

<main id="forms" class="section">
  <div class="container">
    <div class="pack-grid">
{chr(10).join(cards)}
    </div>

    <section class="mt-9" style="max-width:46rem">
      <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">Using these</h2>
      <div class="prose">
        <p>Each form is a standalone page. Copy the markup out of the one you want and
        drop it into your project &#8212; the only requirements are Bootstrap 6&#8217;s CSS and, if
        you use Combobox, Datepicker, OTP, Chips or Range, its JavaScript bundle.</p>
        <p>Bootstrap 6 is ESM-only, so the script tag needs <code>type="module"</code> and
        there is no <code>window.bootstrap</code> global. Importing the bundle for its side
        effects is what registers the data-attribute API.</p>
        <h3>Validation</h3>
        <p><code>.needs-validation</code> and <code>.was-validated</code> are gone. Put
        <code>data-bs-validate</code> and <code>novalidate</code> on the form and native
        <code>:user-invalid</code> handles the styling &#8212; feedback only appears after the
        visitor has actually interacted with a field. Add
        <code>data-bs-validate="valid"</code> if you also want success styling.</p>
        <h3>A gotcha worth knowing</h3>
        <p>Combobox&#8217;s <code>search</code> and <code>multiple</code> options are typed
        booleans, so a bare attribute fails config validation. Write
        <code>data-bs-search="true"</code>, not <code>data-bs-search</code>. Bare marker
        attributes are correct for <code>data-bs-otp</code>, <code>data-bs-chips</code>,
        <code>data-bs-strength</code> and <code>data-bs-validate</code>.</p>
      </div>
    </section>
  </div>
</main>

<footer class="site-footer bg-2 py-6 mt-9">
  <div class="container d-flex flex-wrap justify-content-between align-items-center gap-3">
    <p class="fg-3 fs-xs mb-0">&copy; <span data-year>2026</span> {PACK_TITLE}. A free pack for uicookies.</p>
    <p class="fg-3 fs-xs mb-0">Built with Bootstrap 6.0.0-alpha1</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


for i, v in enumerate(VARIANTS):
    write_variant(i, *v)
write_index()
print(f"wrote index.html + {len(VARIANTS)} variants")
