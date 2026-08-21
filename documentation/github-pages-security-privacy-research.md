# GitHub Pages security and local-file privacy research

Date: 2026-08-21

## Conclusion

GitHub Pages is suitable for this static dashboard only if every published file is safe for public disclosure. The browser can read a user-selected workbook locally without uploading it. That privacy property is not supplied by GitHub Pages itself: it depends on the deployed JavaScript having no form submission or network request that sends the file or its parsed contents.

The locally inspected `index.html` follows that local-only design. It reads a selected CSV with `file.text()` or an XLSX with `file.arrayBuffer()`, keeps imported rows in in-memory JavaScript variables, and does not contain a form submission, `fetch`, `XMLHttpRequest`, `sendBeacon`, WebSocket, EventSource, or `FormData` transmission path. Its only persistent browser storage is `localStorage` for four numeric dashboard settings; imported inventory rows are not written there. Its CSV export uses a browser `Blob` and object URL to download a file to the user's device.

This is a source-code finding for the locally inspected version. The published site remains safe only while the deployed `index.html` matches that reviewed code and no later change introduces an upload, analytics SDK, remote script, service worker, or other network transmission.

## GitHub Pages visibility and transport

- GitHub Pages publishes static HTML, CSS, and JavaScript from a GitHub repository. Anything included in the Pages publishing source should therefore be treated as public website content. [GitHub: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- GitHub explicitly states that a Pages site is publicly available on the internet even when its source repository is private, and advises removing sensitive data before publishing. [GitHub: Securing your GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- GitHub Pages supports HTTPS, and `github.io` sites created after 15 June 2016 are served over HTTPS automatically. HTTPS protects traffic in transit from casual interception or modification; it does not make the public page or repository content confidential. GitHub also says Pages should not be used for sensitive transactions such as passwords or payment-card details. [GitHub: Securing your GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- GitHub records a Pages visitor's IP address for security purposes. [GitHub: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## What a browser file selector does

- An `<input type="file">` lets a user choose files from device storage. The chosen files can be manipulated locally with JavaScript and the File API, or separately uploaded using form submission. Selection alone is not an upload. [MDN: `<input type="file">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file)
- Browser JavaScript can read only files the user explicitly selects through this mechanism; `FileReader` cannot read arbitrary local files by pathname. [MDN: FileReader](https://developer.mozilla.org/en-US/docs/Web/API/FileReader)
- MDN treats local reading and server upload as separate operations. Its upload example adds an explicit `XMLHttpRequest`; reading a selected file does not implicitly perform that request. [MDN: Using files from web applications](https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications)
- Sending file data requires an additional transmission mechanism, such as submitting a form or passing `FormData` to `fetch` or `XMLHttpRequest`. [MDN: Using FormData objects](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest_API/Using_FormData_Objects)

## Audit implications

For every release, verify both the Git repository and the deployed page:

1. The published branch contains no source workbook, CSV export, generated HTML with embedded rows, secrets, or confidential documentation—including in reachable Git history if disclosure has already occurred.
2. The deployed `index.html` starts with an empty dataset and matches the reviewed commit.
3. No first- or third-party code sends selected files, parsed rows, filenames, or inventory-derived values over the network.
4. Browser storage contains only non-sensitive settings; inventory rows are not placed in `localStorage`, `sessionStorage`, IndexedDB, caches, or a service worker.
5. The browser's Network panel shows no request containing file data while importing, filtering, exporting, and refreshing.
6. HTTPS is enforced and the page has no insecure HTTP dependencies.

The strongest runtime confirmation is a clean-browser test with Developer Tools open on the Network and Storage panels. Source inspection establishes intended behavior; a runtime test verifies what the deployed build and browser actually do.
