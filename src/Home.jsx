import React, { useEffect, useState } from "react";
import "./styling/Home.css";
import Hero from "./Hero";

export default function Home() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    const fetchNews = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/get_summarized_news', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_description: 'Your description here' }) // Replace with actual description
      });
      const data = await response.json();
      setNews(data);
    };

    fetchNews();
  }, []);

  return (
    <main className="home">
      <Hero imageUrl='../src/assets/home-hero-img.webp' text='AIdMatch'/>
      <div className="home-content">
        <h2 className="news-title">News</h2>
        <div className="news">
          {news.map((item, index) => (
            <div key={index} className="article">
              <h3 className="article-title">Cluster {item.cluster_id}</h3>
              <p className="article-desc">{item.summary}</p>
              <ul>
                {item.articles.map((article, idx) => (
                  <li key={idx}>
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      {article.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}