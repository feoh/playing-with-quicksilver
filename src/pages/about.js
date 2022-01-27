import * as React from 'react'
import { StaticImage } from 'gatsby-plugin-image'
import Layout from '../components/layout'

const AboutPage = () => {
    return (
        <Layout>
            <StaticImage
                alt="My Picture"
                src="../images/Chris_Brewery.jpg"
                width={640}
                height={480}
                loading="eager"
            />
            <p>Hi! My name's Chris Patti!</p>
            <p>From a very early age, one of my most defining characteristics is that I'm curious about EVERYTHING!</p>
            <p>I love spending time with my lovely wife, my adorable rescue dog Cookie, and my <a href="https://www.amicablelodge.com">lodge brothers.</a></p>
            <p>I think we'll leave it at that for now. I'd like my posts to do most of the talking. Thanks for visiting!</p>

            
        </Layout>
    )

}

export default AboutPage