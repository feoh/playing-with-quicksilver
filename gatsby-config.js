module.exports = {
  siteMetadata: {
      title: `playing-with-quicksilver`,
    siteUrl: `https://playingwithquicksilver.net`
  },
  plugins: ["gatsby-plugin-image", "gatsby-plugin-sharp", "gatsby-transformer-sharp", {
    resolve: 'gatsby-source-filesystem',
    options: {
      "name": "images",
      "path": "./src/images/"
    },
    __key: "images"
  }, {
    resolve: 'gatsby-source-filesystem',
    options: {
      "name": "pages",
      "path": "./src/pages/"
    },
    _key: "pages"
  }, {
      resolve: 'gatsby-source-filesystem',
      options: {
        "name": "blog",
        "path": "./blog/"
      },
      _key: "blog"
  }, {
    resolve: `gatsby-transformer-remark`,
    options: {
      plugins: [
        {
          resolve: `gatsby-remark-images`,
          options: {
            maxWidth: 800,
          },
        },
      ],
    },
  }, {
    resolve: `gatsby-plugin-feed`,
    options: {
      query: `
        {
          site {
            siteMetadata {
              title
              description
              siteUrl
              site_url: siteUrl
            }
          }
        }
      `,
      feeds: [
        {
          serialize: ({ query: { site, allMarkdownRemark } }) => {
            return allMarkdownRemark.nodes.map(node => {
              return Object.assign({}, node.frontmatter, {
                description: node.excerpt,
                date: node.frontmatter.date,
                url: site.siteMetadata.siteUrl + node.fields.slug,
                guid: site.siteMetadata.siteUrl + node.fields.slug,
                custom_elements: [{ "content:encoded": node.html }],
              })
            })
          },
          query: `
            {
              allMarkdownRemark(
                sort: { order: DESC, fields: [frontmatter___date] },
              ) {
                nodes {
                  excerpt
                  html
                  fields { 
                    slug 
                  }
                  frontmatter {
                    title
                    date
                  }
                }
              }
            }
          `,
          output: "/rss.xml",
          title: "Your Site's RSS Feed",
          // optional configuration to insert feed reference in pages:
          // if `string` is used, it will be used to create RegExp and then test if pathname of
          // current page satisfied this regular expression;
          // if not provided or `undefined`, all pages will have feed reference inserted
          match: "^/blog/",
          // optional configuration to specify external rss feed, such as feedburner
          link: "https://feeds.feedburner.com/gatsby/blog",
        },
      ],
    },
  }]
};