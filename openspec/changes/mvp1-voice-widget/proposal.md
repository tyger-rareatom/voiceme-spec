# Proposal: mvp1-voice-widget

## Why
The embeddable widget is the product's "catch" — same script, every site, zero cross-tenant leakage.

## What Changes
Ship `widget.js` loaded via one `<script>` tag with a `data-tenant` attribute; CDN-served, versioned.

## User-visible impact
A tenant pastes one snippet and the branded voice agent appears on their site or mobile-app WebView.

## Rollback
Widget CDN version pinned; rollback to prior bundle.
