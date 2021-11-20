module.exports = {
  siteMetadata: {
    siteUrl: "https://www.yourdomain.tld",
    title: "playing-with-quicksilver",
  },
  plugins: [
    "gatsby-plugin-sitemap",
    "gatsby-plugin-mdx",
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: "pages",
        path: "./src/pages/",
      },
      __key: "pages",
    },
  ],
};
