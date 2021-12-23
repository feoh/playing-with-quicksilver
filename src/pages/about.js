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
            />
            <p>Hi there! My name's Chris Patti.</p>
            <p>I grew up in the 80s playing video games.</p>
            <p>One day, I was sitting there playing some game on my <a href="https://en.wikipedia.org/wiki/Intellivision">Mattel Intellivision</a>, and I had the same epiphany hundreds and thousands of others had around the same time.</p>
            <p>I realized <em>I</em> wanted to be the one controlling the little world playing out behind the TV screen.</p>
            <p>That's when my love affair with computing began.</p>
        </Layout>
    )
}

export default AboutPage