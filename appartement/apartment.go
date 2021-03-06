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
	fmt.Println(calcConsumption(time.Now()))
	conn, err := amqp.Dial("amqp://KVK-T3NDRHs9k9eF:fz9CGA1xCu3zqWCK@10.11.241.45:49977/")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	channel, err := conn.Channel()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	_, err = channel.QueueDeclare("apartment", true, false, false, false, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	background(channel)
}

func calcConsumption(t time.Time) float64 {
	h, m, s := t.Clock()
	secs := h*3600 + m*60 + s
	return 20 + -5*math.Sin(float64(secs)/86400.0*math.Pi*2.0)
}

func writeConsumption(id uint32, consumption float64, ts time.Time) []byte {
	buf := make([]byte, 20)
	binary.BigEndian.PutUint32(buf[:4], id)
	binary.BigEndian.PutUint64(buf[4:12], math.Float64bits(consumption))
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
			msg := writeConsumption(uint32(i), calcConsumption(ts), ts)
			err := (*channel).Publish("", "apartment", false, false, amqp.Publishing{
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
