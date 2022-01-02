import * as React from 'react'
import Layout from '../../components/layout'
import { Link, graphql } from 'gatsby'
import { postListLink, postListDate } from './post-list.module.css'

const BlogPage = ({ data }) => {
    return (
        <Layout>
            {
                data.allMdx.nodes.map(node => (
                    <article key={node.id}>
                        <h2 className={postListLink}>
                            <Link to={`/blog/${node.slug}`}>
                                {node.frontmatter.title}
                            </Link>
                        </h2>
                        <p className={postListDate}>Posted: {node.frontmatter.date}</p>
                    </article>
                ))
            }
        </Layout>
    )
}

export const query = graphql`
    query {
        allMdx(
            sort: {fields: frontmatter___date, order: DESC}
            filter: {frontmatter: {status: {eq: "published"}}}
        ) {
            nodes {
            frontmatter {
                date(formatString: "MMMM D, YYYY")
                title
                status
            }
            id
            slug
            }
        }
    }
`

export default BlogPage