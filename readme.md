<a name="readme-top"></a>

<div align="center">
  <img src="public/logo-dark.png" alt="logo" width="140"  height="auto" />
  <br/>
</div>

# 📗 Table of Contents

- [📖 About the Project](#about-project)
  - [🛠 Built With](#built-with)
    - [Tech Stack](#tech-stack)
    - [Key Features](#key-features)
  - [🚀 Live Demo](#live-demo)
- [💻 Getting Started](#getting-started)
  - [Setup](#setup)
  - [Install](#install)
  - [Usage](#usage)
- [👥 Authors](#authors)
- [🔭 Future Features](#future-features)
- [🤝 Contributing](#contributing)
- [⭐️ Show your support](#support)
- [📝 License](#license)

# 📖 Smart LogiTrack – Urban Transport Predictive System (ETA) <a name="about-project"></a>

Smart LogiTrack is an end-to-end Logistics "Control Tower" designed to predict Estimated Time of Arrival (ETA) for urban transport. This project implements a distributed data architecture that transitions raw taxi data through a Medallion pipeline (Bronze/Silver) to serve real-time machine learning predictions via a secured API.

## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

  <ul>
    <li><a href="https://spark.apache.org/docs/latest/api/python/index.html">PySpark (Distributed ETL)</a></li>
    <li><a href="https://airflow.apache.org/">Apache Airflow (Orchestration)</a></li>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI (ML Serving)</a></li>
    <li><a href="https://www.postgresql.org/">PostgreSQL (Data Warehouse)</a></li>
    <li><a href="https://scikit-learn.org/">Scikit-Learn (ML Modeling)</a></li>
  </ul>

### Key Features <a name="key-features"></a>

- **Distributed ETL Pipeline**: Automated high-volume data cleaning and feature engineering using PySpark.
- **Medallion Architecture**: Structured data flow from raw ingestion (Bronze) to refined ML-ready features (Silver).
- **Automated Orchestration**: End-to-end workflow management and task scheduling via Apache Airflow.
- **Secure Prediction API**: High-performance FastAPI endpoints protected by JWT authentication for safe data access.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Live Demo <a name="live-demo"></a>

- [Project API Documentation](https://github.com/codehass/smart-logitrack)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Getting Started <a name="getting-started"></a>

To get a local copy up and running, follow these steps.

### Setup

Clone this repository to your desired folder:

```sh
  git clone git@github.com:codehass/smart-logitrack.git
```

### Install

Install this project with:

```sh
  cd front-end-next-template
  npm install
```

create `.env` file and add your environment variables. You can copy `.env.example` as a template.

```sh
  cp .env.example .env
```

### Usage

To run the project, execute the following command:

```sh
  npm run dev
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👥 Author <a name="authors"></a>

👤 **Hassan El Ouardy**

- GitHub: [@codehass](https://github.com/codehass)
- Twitter: [@hassanelourdy](https://twitter.com/hassanelourdy)
- LinkedIn: [@hassanelourdy](https://www.linkedin.com/in/hassanelouardy/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🔭 Future Features <a name="future-features"></a>

- **Real-time Streaming**: Integration with Apache Kafka for live taxi data ingestion.
- **Model Monitoring**: Dashboards to track model drift and accuracy over time.
- **Deep Learning**: Implementation of LSTM or Transformer models for temporal traffic patterns.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing <a name="contributing"></a>

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/codehass/the-wild-oasis/issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⭐️ Show your support <a name="support"></a>

Join us in supporting our project to improve cabin management in hotels! Your help makes a big difference in making stays smoother and guests happier. Let's work together to bring positive change to the hospitality industry!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📝 License <a name="license"></a>

This project is [MIT](./MIT.md) licensed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
