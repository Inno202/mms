# Putting the new website live on www.mbusoms.co.za

This folder is the complete website. It runs on the hosting mbusoms.co.za already uses
(Apache with PHP, the usual cPanel set-up). It needs no database.

## 1. Before you start (5 minutes)

1. Sign in to the hosting control panel (cPanel) for mbusoms.co.za.
2. **Back up the current website.** In File Manager open `public_html`, select everything,
   choose **Compress** and download the zip. Keep it, so the old site can be restored
   if needed.
3. Make sure the mailbox **mail@mbusoms.co.za** exists and receives email.
4. Create a mailbox (or forwarder) called **website@mbusoms.co.za**. The forms send from
   this address. Sending from your own domain keeps the messages out of spam.

## 2. Upload

1. In `public_html`, move the old files into a new folder called `old-site`
   (or delete them once the backup zip is safe). Keep any folders the host created,
   such as `cgi-bin` and `.well-known`.
2. Upload `mbusoms-live-upload.zip` into `public_html` and choose **Extract**.
   `index.html`, `send.php`, `.htaccess` and the `css`, `js`, `img` and `fonts`
   folders must sit directly inside `public_html`, not in a sub-folder.
3. If File Manager hides files that start with a dot, turn on **Show hidden files**
   to check that `.htaccess` is there.
4. PHP version: the forms need PHP 7.2 or newer. PHP 8.1 or newer is recommended
   (cPanel → **MultiPHP Manager** or **Select PHP Version**).

## 3. Check it (10 minutes)

1. Open https://www.mbusoms.co.za. The new home page should appear, with the padlock.
2. Open https://www.mbusoms.co.za/index.php and https://www.mbusoms.co.za/contact.php.
   Both should land on the new pages (old links and Google results keep working).
3. Send a test from **Contact** and one from **Learnerships**. Each should say
   "Thank you…" on the page, and the email should arrive in mail@mbusoms.co.za
   within a minute. Press **Reply** on it: it goes to the person who filled in the form.
4. If the email does not arrive, look in the spam folder, then see "If emails do not arrive".
5. Open https://www.mbusoms.co.za/form-config.php. It must show a blank or
   "Forbidden" page, never any settings.

## 4. After it is live

- **Google:** in Google Search Console, add the site and submit
  `https://www.mbusoms.co.za/sitemap.xml`.
- **Changing where forms go:** edit `form-config.php`. `to` is the inbox that receives
  the forms, and `from` is the sending address (it must be on mbusoms.co.za).
- **Spam protection** is built in: a hidden trap field, a minimum time on the page, and
  at most 5 messages per visitor every 15 minutes.

## If emails do not arrive

1. Check the spam folder and add website@mbusoms.co.za to your safe senders.
2. In cPanel → **Email Deliverability**, repair SPF and DKIM for mbusoms.co.za if
   cPanel shows a problem.
3. Some hosts do not allow the sender to be set. In `form-config.php`, change
   `'envelope_sender' => true` to `false` and test again.
4. If the host has switched off PHP `mail()`, ask them to enable it for the domain.

## Undo

Delete the new files from `public_html`, then extract the backup zip from step 1.
