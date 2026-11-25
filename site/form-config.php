<?php
/*
 * Mbuso Management Solutions — website form settings.
 * This file is read by send.php only. The .htaccess file blocks direct access to it.
 *
 * To change who receives website messages, edit 'to'.
 * 'from' must be an address on the website's own domain (for example
 * website@mbusoms.co.za) so mail servers accept the message. Replies go to the
 * visitor, because their address is set as Reply-To.
 */
return [
    'to'                 => 'mail@mbusoms.co.za',
    'from'               => 'website@mbusoms.co.za',
    'from_name'          => 'Mbuso website',

    // Pass the From address to the mail server as the envelope sender (-f).
    // Most cPanel hosts want this on. Turn it off if messages stop sending.
    'envelope_sender'    => true,

    // Anti-spam: at most this many messages per visitor per window (seconds).
    'rate_limit'         => 5,
    'rate_window'        => 900,

    // Anti-spam: forms sent faster than this after the page opened are ignored.
    'min_seconds'        => 3,

    // Forms may only be posted from pages on these hosts (the current host is always allowed).
    'allowed_hosts'      => ['mbusoms.co.za', 'www.mbusoms.co.za'],
];
