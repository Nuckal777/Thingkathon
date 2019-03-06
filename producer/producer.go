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

func main() {
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

func calcOutput(basePower float64, t time.Time) float64 {
	h, m, s := t.Clock()
	secs := h*3600 + m*60 + s
	if secs < 21600 || secs > 64800 {
		return 0
	}
	return basePower * -math.Cos(float64(secs)/86400.0*math.Pi*2.0)
}

func writeProduction(id uint32, prod float64, ts time.Time) []byte {
	buf := make([]byte, 20)
	binary.BigEndian.PutUint32(buf[:4], id)
	binary.BigEndian.PutUint64(buf[4:12], math.Float64bits(prod))
	binary.BigEndian.PutUint64(buf[12:20], uint64(ts.UnixNano()))
	return buf
}

func background(channel *amqp.Channel) {
	dur, err := time.ParseDuration("10s")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	var calcTicker = time.NewTicker(dur)

	for ts := range calcTicker.C {
		for i := 0; i < 4; i++ {
			msg := writeProduction(uint32(i), calcOutput(float64(i*5+5), ts), ts)
			err := (*channel).Publish("", "producer", false, false, amqp.Publishing{
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
