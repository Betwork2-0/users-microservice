# users-microservice

## Back-End Services

### Leveraging Microservice Architecture and Azure Cloud Services

Our project's back-end infrastructure is architected on the foundational principles of a **sophisticated microservice architecture**, ensuring a modular, scalable, and resilient service deployment. Each microservice is intricately designed to serve specific areas of our application, with a primary focus on two crucial domains: **User Data Management** and **NBA Betting Data Aggregation**.

Originally, the goal was to maintain two separate microservices, but for more practical purposes, the nba + user microservices can be found in the 'User Microservices' respository in this project. 

#### User Data Management
This microservice acts as a cornerstone, handling intricate aspects of user authentication, profile management, and personalized user experiences.

#### NBA Betting Data Aggregation
Tailored for the enthusiasts of NBA betting, this microservice is dedicated to aggregating and processing data related to NBA games available for betting.

These microservices are integrated and deployed on **Microsoft Azure**, reflecting our commitment to reliability and continuous service availability. Utilizing Azure's advanced cloud capabilities, like **Azure Kubernetes Service (AKS)** and **Azure Functions**, we have implemented auto-scaling and load balancing features to maintain optimal performance, regardless of traffic fluctuations.

### FastAPI for Advanced API Documentation

Our back-end's efficiency is further enhanced by **FastAPI**, which we use for creating cutting-edge API documentation. FastAPI's swagger UI not only offers a user-friendly interface but also ensures thorough documentation of our API endpoints. This framework has significantly improved our developer experience by offering features like:

- **Auto-generated, interactive API documentation**: Our APIs are self-documenting, with the documentation dynamically updating as endpoints evolve, thanks to Swagger UI.
- **Schema validation and serialization**: Employing Pydantic, FastAPI ensures rigorous schema validation, bolstering data integrity and security.
- **Asynchronous request handling**: FastAPI's support for asynchronous operations allows for efficient, non-blocking request handling, a key factor in maintaining high performance under heavy loads.

Incorporating FastAPI highlights our dedication to adopting best practices in API development and exemplifies our approach to building scalable, efficient, and maintainable back-end services.

![image](https://github.com/Betwork2-0/betworkapp/assets/98557455/725f44ae-7eff-463e-9ff4-712cdaa25cbf)

---

### How to Get the Back-End Running Locally
The cost of azure services was too expensive to justify paying for indefinitely, so in order to test out these features, you'll currently need to clone the Users Microservice repository. 

#### Requirements
To install all the project's dependencies, run: `pip3 install -r requirements.txt` 
- See requirements.txt file.

#### Running and building the app
Run the app: `python3 main.py`  \
Open [http://localhost:5011](http://localhost:5011) to view it in your browser.
To see all endpoints available by Swagger, go to [http://localhost:5011/docs](http://localhost:5011/docs)
New endpoints will be automatically added to Swagger.

