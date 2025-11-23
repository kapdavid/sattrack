# Supabase Setup Guide

This guide will help you set up Supabase authentication for the SatTrack application.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up or log in
2. Click "New Project"
3. Fill in the project details:
   - **Name**: sattrack (or whatever you prefer)
   - **Database Password**: Choose a strong password (save this, though you won't need it for the app)
   - **Region**: Choose the closest region to your users
   - **Pricing Plan**: Free tier is fine for development

4. Click "Create new project" and wait for it to be provisioned (this takes 1-2 minutes)

## Step 2: Configure Authentication

1. In your Supabase project dashboard, go to **Authentication** → **Providers**
2. Make sure **Email** provider is enabled (it should be by default)
3. Configure email settings:
   - You can use Supabase's built-in email service for development
   - For production, you'll want to configure a custom SMTP provider (like Resend)

## Step 3: Get Your API Keys

1. Go to **Settings** → **API** in the Supabase dashboard
2. You'll need three values:

   - **Project URL**: Found under "Project URL" (looks like `https://xxxxx.supabase.co`)
   - **Anon/Public Key**: Found under "Project API keys" → "anon public"
   - **JWT Secret**: Found under "JWT Settings" → "JWT Secret"

## Step 4: Configure Backend Environment Variables

1. Copy the `.env.example` file in the `backend` directory:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-public-key-here
   SUPABASE_JWT_SECRET=your-jwt-secret-here
   ```

## Step 5: Configure Frontend Environment Variables

1. Create a `.env` file in the `frontend` directory:
   ```bash
   cd frontend
   touch .env
   ```

2. Add your Supabase credentials:
   ```
   VITE_SUPABASE_URL=https://your-project-id.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-public-key-here
   ```

## Step 6: Test Authentication

Once you've configured everything:

1. Start the backend server:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

2. Start the frontend dev server:
   ```bash
   cd frontend
   npm run dev
   ```

3. You should be able to sign up and log in through the frontend!

## Security Notes

- **Never commit your `.env` files to Git** - they contain sensitive credentials
- The `.gitignore` file is already configured to exclude them
- The `anon` key is safe to use in frontend code - it has limited permissions
- The `JWT_SECRET` should ONLY be used on the backend - never expose it to the frontend

## Optional: Email Templates

You can customize Supabase's email templates:

1. Go to **Authentication** → **Email Templates**
2. Customize the confirmation, magic link, and password reset emails
3. Add your branding and customize the redirect URLs

## Need Help?

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
