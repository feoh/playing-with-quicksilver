module.exports = {
  siteMetadata: {
    siteUrl: "https://www.yourdomain.tld",
    title: "playing-with-quicksilver",
  },
  plugins: [
    "gatsby-plugin-image",
    "gatsby-plugin-sharp",
    "gatsby-plugin-sitemap",
    "gatsby-plugin-mdx",
    "gatsby-transformer-sharp",
    {
      resolve: "gatsby-source-filesystem",
      options: {
        name: 'blog',
        path: `${__dirname}/blog`,
      },
    }
  ],
};
