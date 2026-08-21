# Hosting this dashboard with GitHub Pages

## Conclusion

Yes. GitHub Pages hosts static HTML, CSS, and JavaScript directly from a GitHub repository, so this repository's generated dashboard is a suitable technical fit. The current `operations-insight.html` is a self-contained static file of about 7.8 MB, well below GitHub Pages' published 1 GB site-size limit.

One important caveat: the HTML embeds the inventory dataset in the page. A GitHub Pages site is publicly available on the internet, even if the source repository is private, so publish it only if that inventory data is safe to disclose. GitHub Pages also does not provide server-side access control or execute PHP, Ruby, or Python. [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

## Recommended setup for this repository

Use branch publishing because the finished dashboard is plain HTML and needs no deployment-time build:

1. Rename or copy `operations-insight.html` to `index.html` in the repository root. GitHub Pages looks for `index.html`, `index.md`, or `README.md` at the top level of the selected publishing source.
2. Push the repository to GitHub. On GitHub Free or GitHub Free for organizations, the repository must be public; private-repository Pages is available on eligible paid plans.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, select **Deploy from a branch**.
5. Select the branch (normally `main`), choose `/(root)`, and save.
6. Wait for publication; GitHub says changes can take up to 10 minutes.

GitHub supports only the repository root or `/docs` as a branch-publishing folder. The existing folder is named `documentation`, so it cannot be selected as the source without reorganizing it. [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) · [Creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

For a normal project repository named `top10-html-analysis`, the default address will be:

```text
https://<github-username>.github.io/top10-html-analysis/
```

A repository named `<github-username>.github.io` instead becomes an account site at `https://<github-username>.github.io/`. Because project sites live below a repository-name path, relative asset links are safer than root-absolute links such as `/styles.css`. The current dashboard appears self-contained, so this path issue should not affect it. [About GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## When to use GitHub Actions instead

Choose **GitHub Actions** as the Pages source if the Python generator should run automatically whenever source data changes, if the published output should be generated rather than committed, or if a custom build is otherwise needed. A Pages workflow must upload the finished site as an artifact with `index.html` at its root and then deploy that artifact. [Custom GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

## Domain and security notes

- GitHub serves `github.io` sites over HTTPS automatically. A correctly configured custom domain can also use **Enforce HTTPS**. [Securing Pages with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- Custom domains are supported. Add the domain in **Settings → Pages** before changing DNS, verify it to reduce takeover risk, and avoid wildcard DNS records. DNS changes can take up to 24 hours. [Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) · [Verifying a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- GitHub Pages is not intended for sensitive transactions, SaaS, e-commerce, or running an online business. Published sites have a 1 GB maximum size, a 10-minute deployment timeout, and soft limits including 100 GB monthly bandwidth. [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
