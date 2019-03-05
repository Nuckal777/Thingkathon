package main

import (
	"fmt"
	"math"
	"os"
	"time"

	"github.com/streadway/amqp"
)

func main() {
	fmt.Println(calcOutput(time.Now()))
	conn, err := amqp.Dial("amqp://KVK-T3NDRHs9k9eF:fz9CGA1xCu3zqWCK@10.11.241.45:49977/")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	channel, err := conn.Channel()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	_, err = channel.QueueDeclare("producer", true, false, false, false, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	background(channel)
}

func calcOutput(t time.Time) float64 {
	h, m, s := t.Clock()
	secs := h*3600 + m*60 + s
	if secs < 21600 || secs > 64800 {
		return 0
	}
	return 20 * -math.Cos(float64(secs)/86400.0*math.Pi*2.0)
}

func background(channel *amqp.Channel) {
	dur, err := time.ParseDuration("1s")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	var calcTicker = time.NewTicker(dur)

	for ts := range calcTicker.C {
		err := (*channel).Publish("", "producer", false, false, amqp.Publishing{
			Headers:         amqp.Table{},
			ContentType:     "text/plain",
			ContentEncoding: "",
			Body:            []byte(fmt.Sprint(calcOutput(ts))),
			DeliveryMode:    amqp.Persistent,
			Priority:        0,
		})
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
		fmt.Println("delivered message")
	}
}
