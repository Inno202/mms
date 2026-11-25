<?php
/*
 * Mbuso Management Solutions — form handler.
 * Receives the contact form and the learnership registration form, checks every
 * field on the server, and emails the entry to the address in form-config.php.
 * Nothing is stored except a short-lived, hashed counter per visitor for rate limiting.
 *
 * Works two ways:
 *  - with JavaScript: the page posts here with "Accept: application/json" and gets JSON back;
 *  - without JavaScript: a normal form post, answered with a redirect to thanks.html
 *    (or back to the form with ?status=error).
 * Compatible with PHP 7.2 and newer.
 */
declare(strict_types=1);

$config = require __DIR__ . '/form-config.php';

header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('Cache-Control: no-store');

$accept   = isset($_SERVER['HTTP_ACCEPT']) ? (string) $_SERVER['HTTP_ACCEPT'] : '';
$wantJson = strpos($accept, 'application/json') !== false;

function respond(bool $wantJson, int $status, array $data, string $redirect): void
{
    if ($wantJson) {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($data);
    } else {
        header('Location: ' . $redirect, true, 303);
    }
    exit;
}

/* ---- 1. Method, size and origin ---- */
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond($wantJson, 405, ['ok' => false, 'error' => 'method'], 'contact.html');
}
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 20000) {
    respond($wantJson, 413, ['ok' => false, 'error' => 'too_large'], 'contact.html?status=error');
}
$host    = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
$allowed = array_map('strtolower', array_merge([$host], (array) $config['allowed_hosts']));
foreach (['HTTP_ORIGIN', 'HTTP_REFERER'] as $h) {
    if (!empty($_SERVER[$h])) {
        $from = strtolower((string) parse_url((string) $_SERVER[$h], PHP_URL_HOST));
        $port = parse_url((string) $_SERVER[$h], PHP_URL_PORT);
        if ($port) { $from .= ':' . $port; }
        $bare = preg_replace('/:\d+$/', '', $from);
        if (!in_array($from, $allowed, true) && !in_array($bare, $allowed, true)) {
            respond($wantJson, 403, ['ok' => false, 'error' => 'origin'], 'contact.html?status=error');
        }
        break;
    }
}

/* ---- 2. Which form ---- */
$form = (string) ($_POST['form'] ?? '');
$forms = [
    'contact' => [
        'page'    => 'contact.html',
        'subject' => 'Website enquiry',
        'fields'  => [
            'name'         => ['label' => 'Name',         'max' => 80,   'required' => true],
            'phone'        => ['label' => 'Phone',        'max' => 20,   'required' => false, 'type' => 'phone'],
            'email'        => ['label' => 'Email',        'max' => 120,  'required' => true,  'type' => 'email'],
            'organisation' => ['label' => 'Organisation', 'max' => 120,  'required' => false],
            'topic'        => ['label' => 'Topic',        'required' => true, 'allowed' => ['Strategy and consulting', 'Training and skills development', 'Industrial operations and the Hub', 'Partnerships and CSI', 'Something else']],
            'message'      => ['label' => 'Message',      'min' => 10,  'max' => 2000, 'required' => true, 'multiline' => true],
        ],
        'subject_field' => 'topic',
    ],
    'learnership' => [
        'page'    => 'learnerships.html',
        'subject' => 'Learnership interest',
        'fields'  => [
            'name'          => ['label' => 'Name',                  'max' => 80,  'required' => true],
            'phone'         => ['label' => 'Cellphone',             'max' => 20,  'required' => true,  'type' => 'phone'],
            'email'         => ['label' => 'Email',                 'max' => 120, 'required' => false, 'type' => 'email'],
            'town'          => ['label' => 'Town or city',          'max' => 60,  'required' => true],
            'field'         => ['label' => 'Field of interest',     'required' => true, 'allowed' => ['Trades and energy', 'Water and wastewater', 'Agriculture', 'Clothing and furniture', 'Computers and IT', 'Business and safety', 'Not sure yet']],
            'qualification' => ['label' => 'Highest qualification', 'required' => true, 'allowed' => ['Below Grade 12', 'Grade 12 (matric)', 'Certificate or diploma', 'Degree']],
            'message'       => ['label' => 'Message',               'max' => 1000, 'required' => false, 'multiline' => true],
        ],
        'subject_field' => 'field',
    ],
];
if (!isset($forms[$form])) {
    respond($wantJson, 400, ['ok' => false, 'error' => 'form'], 'contact.html?status=error');
}
$spec = $forms[$form];
$back = $spec['page'];

/* ---- 3. Bots: honeypot and speed ---- */
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    // Pretend it worked so the bot learns nothing.
    respond($wantJson, 200, ['ok' => true], 'thanks.html?form=' . $form);
}
$started = (int) ($_POST['t'] ?? 0);  // set by the page's script; absent without JavaScript
if ($started > 0) {
    $elapsed = (int) floor(microtime(true) * 1000) - $started;
    if ($elapsed >= 0 && $elapsed < ((int) $config['min_seconds']) * 1000) {
        respond($wantJson, 200, ['ok' => true], 'thanks.html?form=' . $form);
    }
}

/* ---- 4. Rate limit (hashed IP, short-lived file) ---- */
$dir = rtrim(sys_get_temp_dir(), '/\\') . DIRECTORY_SEPARATOR . 'mbuso-forms';
if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
$ip     = (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$bucket = $dir . DIRECTORY_SEPARATOR . hash('sha256', $ip . '|' . __DIR__) . '.json';
$now    = time();
$hits   = [];
if (is_file($bucket)) {
    $saved = json_decode((string) @file_get_contents($bucket), true);
    if (is_array($saved)) {
        foreach ($saved as $t) {
            if (is_int($t) && $t > $now - (int) $config['rate_window']) { $hits[] = $t; }
        }
    }
}
if (count($hits) >= (int) $config['rate_limit']) {
    respond($wantJson, 429, ['ok' => false, 'error' => 'rate'], $back . '?status=busy');
}

/* ---- 5. Validate every field ---- */
function clean_line(string $v): string
{
    // One line only: strips CR/LF and control characters, which also stops header injection.
    $v = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v);
    return trim(preg_replace('/\s+/u', ' ', (string) $v));
}
function clean_text(string $v): string
{
    $v = str_replace(["\r\n", "\r"], "\n", $v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/u', '', $v);
    return trim((string) $v);
}
function text_length(string $v): int
{
    return function_exists('mb_strlen') ? mb_strlen($v, 'UTF-8') : strlen(utf8_decode($v));
}

$values = [];
$errors = [];
foreach ($spec['fields'] as $key => $rule) {
    $raw = isset($_POST[$key]) && is_string($_POST[$key]) ? $_POST[$key] : '';
    if (!preg_match('//u', $raw)) { $raw = ''; }                 // reject invalid UTF-8
    $v   = !empty($rule['multiline']) ? clean_text($raw) : clean_line($raw);
    $len = text_length($v);
    if ($v === '') {
        if (!empty($rule['required'])) { $errors[$key] = 'required'; }
        $values[$key] = '';
        continue;
    }
    if (isset($rule['max']) && $len > $rule['max'])        { $errors[$key] = 'too_long'; }
    elseif (isset($rule['min']) && $len < $rule['min'])    { $errors[$key] = 'too_short'; }
    elseif (isset($rule['allowed']) && !in_array($v, $rule['allowed'], true)) { $errors[$key] = 'invalid'; }
    elseif (($rule['type'] ?? '') === 'email' && !filter_var($v, FILTER_VALIDATE_EMAIL)) { $errors[$key] = 'invalid'; }
    elseif (($rule['type'] ?? '') === 'phone' && !preg_match('/^[+0-9 ()-]{9,20}$/', $v)) { $errors[$key] = 'invalid'; }
    $values[$key] = $v;
}
if (($_POST['consent'] ?? '') !== 'yes') { $errors['consent'] = 'required'; }

if ($errors) {
    respond($wantJson, 422, ['ok' => false, 'error' => 'invalid', 'fields' => $errors], $back . '?status=error');
}

/* ---- 6. Compose and send ---- */
$subjectText = $spec['subject'] . ': ' . $values[$spec['subject_field']] . ' (' . $values['name'] . ')';
$subject     = '=?UTF-8?B?' . base64_encode($subjectText) . '?=';

$lines = [];
foreach ($spec['fields'] as $key => $rule) {
    if ($key === 'message') { continue; }
    $lines[] = str_pad($rule['label'] . ':', 24) . ($values[$key] !== '' ? $values[$key] : '-');
}
$body  = $spec['subject'] . " from the website\n";
$body .= str_repeat('-', 40) . "\n";
$body .= implode("\n", $lines) . "\n";
if (($values['message'] ?? '') !== '') {
    $body .= "\nMessage:\n" . $values['message'] . "\n";
}
$body .= "\n" . str_repeat('-', 40) . "\n";
$when = new DateTime('now', new DateTimeZone('Africa/Johannesburg'));
$body .= 'Sent ' . $when->format('j F Y, H:i') . " (South African time) from the form on " . $back . ".\n";
$body .= "The visitor agreed to be contacted about this request (POPIA consent).\n";
$body .= ($values['email'] ?? '') !== '' ? "Reply to this email to answer them directly.\n" : "No email address given: reply by phone.\n";

$fromName = '=?UTF-8?B?' . base64_encode((string) $config['from_name']) . '?=';
$headers   = [];
$headers[] = 'From: ' . $fromName . ' <' . $config['from'] . '>';
if (($values['email'] ?? '') !== '') {
    $replyName = '=?UTF-8?B?' . base64_encode($values['name']) . '?=';
    $headers[] = 'Reply-To: ' . $replyName . ' <' . $values['email'] . '>';
}
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'Content-Transfer-Encoding: 8bit';
$headers[] = 'X-Mailer: Mbuso website form';

$params = !empty($config['envelope_sender']) ? '-f' . $config['from'] : '';
$sent   = $params !== ''
    ? @mail((string) $config['to'], $subject, $body, implode("\r\n", $headers), $params)
    : @mail((string) $config['to'], $subject, $body, implode("\r\n", $headers));

if (!$sent) {
    respond($wantJson, 502, ['ok' => false, 'error' => 'send_failed'], $back . '?status=error');
}

$hits[] = $now;
@file_put_contents($bucket, json_encode($hits), LOCK_EX);

respond($wantJson, 200, ['ok' => true], 'thanks.html?form=' . $form);
