# book-system API

## Introduction
The Book-Service API is a tool designed for cinemas and theaters to manage events, rooms, and seat bookings. It simplifies event scheduling, room configuration, and seat reservations, making it easy for entertainment venues to enhance their operations and provide a seamless booking experience for customers

## Key Features
- Event Management: This API provides robust capabilities for creating and managing events. Events could represent various performances, shows, or film screenings, allowing venues to offer a wide range of entertainment options.

- Room Configuration: Venues can create, configure, and manage rooms to accommodate different types of events. Whether it's a small theater for an intimate play or a large cinema hall for blockbuster movies, the API has you covered.

- Seat Booking: With the Book-Service API, integrating seat booking logic into your platform is a breeze. API simplifies the process, ensuring a seamless and user-friendly seat booking experience for your customers.

## Getting Started
To quickly set up and run the Book-Service API on your local development environment, we recommend using Docker Compose. This method streamlines the setup process and ensures that all required services are running in a consistent environment.

### Configuration
Clone the repository to your local machine:

```bash
git clone git@github.com:kradt/book-system.git
```
Navigate to the project directory:

```bash
cd book-service-api
```
Create a .env file in the project directory to store configuration variables. Populate the .env file with the necessary environment variables specific to your setup. Here is one essential variable:

```
DATABASE_URL=your-database-url
```
DATABASE_URL should be the connection URL for your database.

### Prerequisites
Before you begin, make sure you have the following prerequisites installed on your system:

`Docker`
`Docker Compose`

### Running with Docker Compose
1. Start the application using Docker Compose:

```bash
docker-compose up -d
```
2. The API should now be running. You can access it at http://localhost:5000/

3. Explore the API and its endpoints. You can find detailed API documentation and examples in our Swagger documentation at http://localhost:5000/docs or the URL where your Swagger documentation is hosted.

### Stopping the Application
To stop the application and remove the containers, run:
```bash
docker-compose down
```

That's it! You're now ready to start using the Book-Service API with Docker Compose on your local machine.
