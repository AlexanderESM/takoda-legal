# Privacy implementation review

Prepared on 17 October 2026 against The Art of Dining 1.1.0 / versionCode 25, Android source commit `6c7f7b5`.

## Verified from the application

- Package/namespace: `com.takodadigital.theartofdining`; no account, login, developer-hosted backend, purchases, subscriptions, configured Firebase Analytics or Crashlytics integration was found.
- Direct manifest permissions: INTERNET and ACCESS_NETWORK_STATE. The inspected compiled release manifest additionally contains AD_ID, ACCESS_ADSERVICES_AD_ID, ACCESS_ADSERVICES_ATTRIBUTION, ACCESS_ADSERVICES_TOPICS, WAKE_LOCK and FOREGROUND_SERVICE from dependencies, plus the app's internal receiver permission. The SDK manifest includes MobileAdsInitProvider. Do not infer zero startup SDK activity merely because explicit game ad calls are lazy.
- Dependency: Google Mobile Ads SDK 25.5.0. Resolved release dependencies include `user-messaging-platform:4.0.0`, `play-services-measurement-sdk-api:20.1.2`, advertising-identifier and app-set components. UMP being present transitively is not an implemented consent flow.
- No `UserMessagingPlatform` consent API call, consent-state gate, privacy-options entry or personalised-advertising preference was found. Requests use `AdRequest.Builder().build()`.
- Demo application ID: `ca-app-pub-3940256099942544~3347511713`; rewarded unit: `ca-app-pub-3940256099942544/5224354917`; interstitial unit: `ca-app-pub-3940256099942544/1033173712`. These remain unchanged, including release builds.
- Hints are free for bundled serving levels 1–3. Interstitial and rewarded eligibility starts with later content, which is not yet bundled. This does not prove that Google's SDK performs no automatic processing.
- BreakfastProgress stores current level, completed levels and stage IDs in private SharedPreferences. DrinksProgress stores completed drink indexes. AdProgressStore stores active-play duration, unique wins and advertising-frequency counters locally. No progress upload was found. `allowBackup=false` is configured.
- No in-app privacy-policy URL or external-link flow was found. Settings currently shows app/version information. There is no account-deletion service, in-app local-data deletion button or in-app consent form. Local storage can be removed through Android app settings or uninstalling.
- Explicit diagnostic logging uses local Android Log calls for SDK failures. The Google SDK has its own documented diagnostics/measurement behaviour; its complete network behaviour was not independently audited.

Source evidence: `app/src/main/AndroidManifest.xml`, `app/build.gradle.kts`, AdMobRewardedHintProvider.kt, AdMobTransitionProvider.kt, InterstitialSchedule.kt, ServingHints.kt, BreakfastProgress.kt, DrinksProgress.kt, AdProgressStore.kt, AppNavigationScreen.kt, the resolved release dependency report and the inspected release-bundle manifest.

## Verified project details supplied by the developer

Alexander Orekhov; brand Takoda Digital; Cyprus; takodadigital@gmail.com; audience 18+; The Art of Dining. The website does not invent a company registration, postal address or age-verification feature.

## Material issues still requiring attention

1. **Hosting/authentication:** GitHub CLI is absent and no authenticated account was established. Publication has not happened. There is no verified live URL to paste into Play Console yet. The policy date is prepared as 17 October 2026; update it with `prepare_publication.py` on the actual publication day.
2. **In-app access:** add an accessible policy entry after obtaining the verified final URL. This local-only task has not changed Android source or the existing signed AAB.
3. **Consent:** the presence of a UMP dependency does not satisfy consent management. Review the countries served, Google's current requirements and applicable law, and implement/verify consent gating and privacy options where required before production advertising. A voluntary rewarded-advert confirmation is not privacy consent.
4. **Data safety:** the Google Mobile Ads SDK documents identifier, interaction, IP/general-location and diagnostic processing. Confirm the exact configuration and data flows, then complete Data safety consistently. Do not answer that no data is collected solely because there are no accounts or because demo advert IDs are used.
5. **Advertising setup:** current IDs are Google's demo values. Review the production AdMob app/unit setup separately; no IDs or request behaviour were changed here.
6. **Age/audience:** 18+ is the supplied intended audience, not an implemented age gate. Review the Play target-audience declaration and advertising configuration without assuming the source currently enforces adult-only access.
7. **Retention, rights and international processing:** the policy distinguishes local data, correspondence controlled by the developer and third-party processing. Confirm the developer's actual email-handling/retention practice and relevant legal obligations. It does not guarantee deletion of Google's records or that all processing remains in Cyprus.
8. **Technical checks are limited:** static validation does not certify legal compliance, global reach, SDK network behaviour or Google's acceptance of a Play submission. HTTPS/login-free access can only be confirmed after deployment.

## References checked

- Google Play User Data policy: https://support.google.com/googleplay/android-developer/answer/10144311?hl=en
- Google Mobile Ads data disclosure (25.5.0): https://developers.google.com/admob/android/privacy/play-data-disclosure
- Google UMP integration and request gating: https://developers.google.com/admob/android/privacy
- Google's Privacy Policy: https://policies.google.com/privacy
- GitHub Pages branch/root publishing: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub hosting privacy: https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement
- European Commission individual data-protection rights: https://commission.europa.eu/law/law-topic/data-protection/information-individuals_en

No source code, signing key, password, private certificate, token, AAB or APK is included in this website repository. The contact email and developer identity are intentionally public.

## Validation performed

Five offline tests passed: semantic HTML structure/language, local hyperlinks and fragment targets, all 15 policy sections and project details, absence of tracking/remote assets, and absence of key/bundle files or unresolved public-page placeholders. All three maintenance scripts compiled successfully.

Policy desktop rendering was visually inspected at 1440 px. A dedicated 390 px iframe was used to verify the true mobile CSS viewport independently of the headless browser's minimum outer-window width. The landing page was inspected at desktop width. The body, secondary text, link, pill and button colour pairs have contrast ratios of 11.56, 5.89, 7.64, 7.68 and 12.09 respectively, all above 4.5:1. Heading hierarchy, skip navigation and visible keyboard-focus styles are present. These are accessibility basics, not a full assistive-technology certification.

The three distinct external destinations used by the public pages (Google Privacy Policy, Google's SDK data disclosure and GitHub Privacy Statement) were opened successfully during preparation. Email delivery was not tested, and no message was sent. No live GitHub Pages source, public TLS endpoint or geographic reach was available to validate. There is no published repository URL or Google Play policy URL yet.

Android source, saved progress, package, version and signing material were unchanged. A read-only Gradle release-dependency report was generated for inspection; no Android build/device regression run is claimed for this website-only task. Existing version 1.1.0 remains the source of the inspected app.
