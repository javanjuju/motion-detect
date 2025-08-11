import express, { NextFunction, Request, Response } from "express";
import { Server } from "socket.io";
import http from "http";
import fs from "fs";

// Create an Express app and HTTP server
const app = express();
const httpServer = http.createServer(app);
const io = new Server(httpServer, {
	cors: {
		origin: "*",
		allowedHeaders: "*",
	},
});

app.get("/", (req: Request, res: Response, next: NextFunction) => {
	res.send({ message: "Welcome to the server" }).status(200);
});

io.on("connection", socket => {
	console.log(`Client connected. ID ${socket.id}`);

	socket.on("motion-detected", data => {
		io.emit("motion-detected", data);
	});

	socket.on("disconnect", () => {
		console.log("Client disconnected");
	});
});

httpServer.listen(3000, () => console.log("Server Started"));
