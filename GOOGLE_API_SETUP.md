# 🔑 How to Get Google API Credentials for SEO AI OS

To allow your central SEO email (`seo@example.com`) to automatically pull Search Console (GSC) and Google Analytics (GA4) data for all your clients, you need to generate a `Client ID` and `Client Secret`. 

This is a **one-time setup**. Once added to your `.env` file, the AI OS will be able to access data for *any* client property that `seo@example.com` has permission to view.

Follow these exact steps:

---

## Phase 1: Create a Google Cloud Project

1. Open your browser and go to the **Google Cloud Console**: https://console.cloud.google.com/
2. Ensure you are logged in with **seo@example.com**.
3. In the top-left navigation bar, click the project dropdown (it may say "Select a project") and click **New Project**.
4. **Project Name:** `SEO-AI-OS-Data` (or anything you prefer).
5. Leave "Organization" and "Location" as they are (or "No Organization").
6. Click **Create** and wait a few seconds.
7. Once created, click the notification or the top project dropdown to **select your new project**.

---

## Phase 2: Enable the APIs

You need to tell Google Cloud what this project is allowed to fetch.

1. In the left sidebar menu, go to **APIs & Services** > **Library**.
2. In the search bar, type `Google Search Console API`.
3. Click on the result and click the blue **Enable** button.
4. Go back to the Library and search for `Google Analytics Data API`.
5. Click on the result and click **Enable**.

---

## Phase 3: Configure the OAuth Consent Screen

Before you can create keys, Google needs to know who is using the app.

1. Go to **APIs & Services** > **OAuth consent screen** in the left menu.
2. Select **External** as the User Type (unless your email is part of a Google Workspace, then select **Internal**). Click **Create**.
3. Fill out the required App information:
   - **App name:** `SEO AI OS`
   - **User support email:** `seo@example.com`
   - **Developer contact information:** `seo@example.com`
   - *You can leave the rest blank.*
4. Click **Save and Continue**.
5. On the **Scopes** page, just click **Save and Continue** (we don't need to specify scopes here).
6. On the **Test users** page, click **+ Add Users**.
7. Type in `seo@example.com` and click **Add**.
   - *Note: Since your app is in "Testing" mode, only the emails added here can authenticate. You just need to add yourself.*
8. Click **Save and Continue**, then **Back to Dashboard**.

---

## Phase 4: Create the API Credentials

Now we generate the actual keys.

1. In the left menu, go to **APIs & Services** > **Credentials**.
2. Click **+ Create Credentials** at the top, and select **OAuth client ID**.
3. **Application type:** Select **Desktop app** (since you are running this locally in VS Code).
4. **Name:** `Claude Code OS` (or anything).
5. Click **Create**.
6. A popup will appear containing your **Client ID** and **Client Secret**.

---

## Phase 5: Add Keys to Your `.env` File

1. Open the `.env` file in your IDE (or copy `.env.example` to `.env` if you haven't already).
2. Paste the keys exactly as shown:

```ini
GOOGLE_CLIENT_ID=your-long-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_PROJECT_ID=seo-ai-os-data-123456  # Make sure this matches your project ID
```

*(You can find the `GOOGLE_PROJECT_ID` by clicking the project name at the very top of Google Cloud Console. It's usually the name followed by some numbers).*

---

## Phase 6: The First Run Authentication

The very first time you run an `/audit` or `/monthly_report` for a client that requires GSC data, the Python script will suddenly open a new tab in your web browser.

1. Google will ask you to sign in. **Choose `seo@example.com`.**
2. It will warn you that "Google hasn't verified this app." This is completely fine—*you* built the app. Click **Advanced**, then **Go to SEO AI OS (unsafe)**.
3. Check the boxes to grant access to Search Console and Google Analytics data.
4. Click **Continue**.

The browser window will close, and your terminal will say "Authentication successful!" It will save a tiny `token.json` file in your folder so that you **never have to log in manually again.** 

From then on, the OS will instantly pull data for any client.
