# 🛒 OrderStream

OrderStream is a lightweight, containerized, event-driven order processing system. It demonstrates microservice architecture using **Kafka**, **PostgreSQL**, and **Python-based APIs**, with a simple **frontend UI**.

---

## 📦 Features

- Submit orders via a web UI
- Order flow through Kafka topics: `orders-new` → `orders-processed`
- Multiple Python microservices for API, processing, and persistence
- Data stored in PostgreSQL
- Easily extensible and fully containerized with Docker

---

## 🧱 Architecture

