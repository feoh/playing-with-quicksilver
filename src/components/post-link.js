import React from "react"
import { Link } from "gatsby"
import { postListLink, postListDate } from './post-list.module.css'

const PostLink = ({ post }) => (
    <article>
        <h2 className={postListLink}>
            <Link to={post.frontmatter.slug}>
                {post.frontmatter.title}
            </Link>
        </h2>
        <p className={postListDate}>
            {post.frontmatter.date}
        </p>
    </article>
)

export default PostLink