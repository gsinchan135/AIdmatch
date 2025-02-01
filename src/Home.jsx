import React from "react";
import "./styling/Home.css";
import Hero from "./Hero";

export default function Home() {
  return (
      <main className="home">
        <Hero imageUrl='../src/assets/home-hero-img.webp' text='AIdMatch'/>
        <div className="home-content">
          <h2 className="news-title">News</h2>
          <div className="news">
            <div className="article">
              <h3 className="article-title">Article Title 1</h3>
              <p className="article-date">Date: 2025-02-01</p>
              <p className="article-desc">Description of the event goes here.</p>
            </div>
            <div className="article">
              <h3 className="article-title">Article Title 2</h3>
              <p className="article-date">Date: 2025-02-02</p>
              <p className="article-desc">Another event description here.</p>
            </div>
            <div className="article">
              <h3 className="article-title">Article Title 3</h3>
              <p className="article-date">Date: 2025-02-03</p>
              <p className="article-desc">More details about this event.</p>
            </div>
          </div>
        </div>
      </main>
  );
}
