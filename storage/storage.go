package main

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"math"
	"os"
	"time"

	"github.com/streadway/amqp"
)

type Storage struct {
	ID        uint32
	Capacity  float64
	MaxCap    float64
	Available bool
}

var allStorage [4]Storage

func main() {
	//init Storage
	for i := 0; i < len(allStorage); i++ {
		allStorage[i] = Storage{
			Available: true,
			MaxCap:    float64(i)*7.0 + 10.0,
			Capacity:  float64(i)*2.0 + 5.0,
			ID:        uint32(i),
		}
	}
	//init Connections
	connSend, err := amqp.Dial("amqp://KVK-T3NDRHs9k9eF:fz9CGA1xCu3zqWCK@10.11.241.45:49977/")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	channelSend, err := connSend.Channel()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	_, err = channelSend.QueueDeclare("status", true, false, false, false, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}

	connRecive, err := amqp.Dial("amqp://KVK-T3NDRHs9k9eF:fz9CGA1xCu3zqWCK@10.11.241.45:49977/")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	channelRecive, err := connRecive.Channel()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	_, err = channelRecive.QueueDeclare("charge", true, false, false, false, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	deliveryChan, err := channelRecive.Consume("charge", "storage", true, false, false, false, nil)
	go background(channelSend)
	for packet := range deliveryChan {
		buf := packet.Body
		id := binary.BigEndian.Uint32(buf[0:4])
		charge := math.Float64frombits(binary.BigEndian.Uint64(buf[4:12]))
		allStorage[id].Capacity += charge
		fmt.Println("Updated ", id, " to new capacity: ", charge)
	}
}

func writeStorage(storage *Storage, ts time.Time) []byte {
	buf := make([]byte, 24)
	binary.BigEndian.PutUint32(buf[:4], storage.ID)
	binary.BigEndian.PutUint64(buf[4:12], uint64(storage.Capacity))
	binary.BigEndian.PutUint64(buf[12:20], uint64(ts.UnixNano()))
	aValue := 0
	if storage.Available {
		aValue = 1
	}
	binary.BigEndian.PutUint32(buf[20:24], uint32(aValue))
	return buf
}

func background(channel *amqp.Channel) {
	dur, err := time.ParseDuration("10s")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	var calcTicker = time.NewTicker(dur)

	for ts := range calcTicker.C {
		for i := 0; i < len(allStorage); i++ {
			msg := writeStorage(&allStorage[i], ts)
			err := (*channel).Publish("", "status", false, false, amqp.Publishing{
				Headers:         amqp.Table{},
				ContentType:     "text/plain",
				ContentEncoding: "",
				Body:            msg,
				DeliveryMode:    amqp.Persistent,
				Priority:        0,
			})
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
			}
			fmt.Println("delivered message ", hex.EncodeToString(msg))
		}
	}
}
