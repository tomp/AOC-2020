package main

import (
	"fmt"
	// "math"
	"os"
	"strings"
)

type LinkedList struct {
	value int
	prev  *LinkedList
	next  *LinkedList
}

var exampleLabels = []int{3, 8, 9, 1, 2, 5, 4, 6, 7}
var inputLabels = []int{5, 3, 8, 9, 1, 4, 7, 6, 2}

// buildRing bulds a circular linked list of a specified size, and starting
// with the given labels.
func buildRing(labels []int, size int) *LinkedList {
	maxVal := 0
	count := 0
	last := &LinkedList{labels[0], nil, nil}
	first := last
	for _, v := range labels[1:] {
		node := &LinkedList{v, last, nil}
		last.next = node
		last = node
		if v > maxVal {
			maxVal = v
		}
		count += 1
	}

	for v := maxVal + 1; count < size-1; v = v + 1 {
		node := &LinkedList{v, last, nil}
		last.next = node
		last = node
		count += 1
	}

	last.next = first
	first.prev = last

	return first
}

// size() returns the siz of the given list, whether circular or linear
func (v *LinkedList) size() int {
	if v == nil {
		return 0
	}
	p := v
	result := 1
	for p.next != nil && p.next != v {
		result += 1
		p = p.next
	}
	return result
}

// print() prints the values of the given list
func (v *LinkedList) print(currValue int) {
	p := v
	for p != nil {
		if p.value == currValue {
			fmt.Printf("(%d) ", p.value)
		} else {
			fmt.Printf("%d ", p.value)
		}
		if p.next == v {
			break
		}
		p = p.next
	}
	fmt.Println()
}

// toString() prints the values of the given list
func (v *LinkedList) toString(sep string) string {
	var labels []string
	labels = append(labels, fmt.Sprintf("%d", v.value))
	p := v.next
	for p != nil && p != v {
		labels = append(labels, fmt.Sprintf("%d", p.value))
		p = p.next
	}
	return strings.Join(labels, "")
}

// printSubset() prints a subset of the values of the given list
func (v *LinkedList) printSubset(currValue int) {
	if v.prev != nil {
		fmt.Printf("%d ", v.prev.value)
	}
	p := v
	for count := 0; count < 6; count++ {
		if p.value == currValue {
			fmt.Printf("(%d) ", p.value)
		} else {
			fmt.Printf("%d ", p.value)
		}
		if p.next == v || p.next == nil {
			break
		}
		p = p.next
	}
	fmt.Println()
}

// forward() returns a pointer to the node 'count' steps forward from the current node
func (v *LinkedList) forward(count int) *LinkedList {
	result := v
	for i := 0; i < count; i++ {
		result = result.next
		if result == nil {
			break
		}
	}
	return result
}

// backward() returns a pointer to the node 'count' steps backward from the current node
func (v *LinkedList) backward(count int) *LinkedList {
	result := v
	for i := 0; i < count; i++ {
		result = result.prev
		if result == nil {
			break
		}
	}
	return result
}

// cut() removes a specified number of nodes from the list, starting with the node
// following the current node.  A pointer to the nodes that were removed is returned.
func (v *LinkedList) cut(count int) *LinkedList {
	result := v.next
	result.prev = nil
	p := v.next
	for i := 0; i < count-1; i++ {
		p = p.next
	}
	v.next = p.next
	v.next.prev = v
	p.next = nil
	return result
}

// insert() inserts the given list into this list, after the current position.
func (v *LinkedList) insert(list *LinkedList) {
	after := v.next
	v.next = list
	list.prev = v
	p := list
	for p.next != nil {
		p = p.next
	}
	p.next = after
	after.prev = p
}

// findNext() returns a pointer to the node with the specified value
func (v *LinkedList) findNext(target int) *LinkedList {
	p := v
	for p.value != target && p.next != nil && p.next != v {
		p = p.next
	}
	if p.value != target {
		return nil
	}
	return p
}

// find2() returns a pointer to the node with the specified value
func (v *LinkedList) findPrev(target int) *LinkedList {
	p := v
	for p.value != target && p.prev != nil && p.prev != v {
		p = p.prev
	}
	if p.value != target {
		return nil
	}
	return p
}

// move() plays out one move of the crab game.  A pointer to the next current value is
// returned.
func (v *LinkedList) play_move(maxValue int) *LinkedList {
	three := v.cut(3)
	// fmt.Printf("pick up ")
	// three.print(0)

	var destValue int
	if v.value > 1 {
		destValue = v.value - 1
	} else {
		destValue = maxValue

	}
	for three.findNext(destValue) != nil {
		if destValue > 1 {
			destValue = destValue - 1
		} else {
			destValue = maxValue
		}
	}
	// fmt.Printf("destination: %d\n", destValue)
	dest := v.findPrev(destValue)
	// dest.printSubset(0)

	dest.insert(three)
	return v.next
}

func play_game(labels []int, moves int) string {
	var cups, curr, three, dest *LinkedList
	var destValue int

	cups = buildRing(labels, 0)
	size := cups.size()
	if size != len(labels) {
		fmt.Printf("Ring size is %d (expected %d)", size, len(labels))
		os.Exit(1)
	}
	fmt.Printf("play_game: %d cups, %d moves\n", size, moves)
	curr = cups
	curr.print(curr.value)

	for move := 0; move < moves; move++ {
		fmt.Printf("\n-- move %d --\n", move+1)
		curr.printSubset(curr.value)
		three = curr.cut(3)
		fmt.Printf("pick up ")
		three.print(0)

		if curr.value > 1 {
			destValue = curr.value - 1
		} else {
			destValue = size
		}
		for destValue == three.value || destValue == three.next.value ||
			destValue == three.next.next.value {
			if destValue > 1 {
				destValue = destValue - 1
			} else {
				destValue = size
			}
		}
		fmt.Printf("destination: %d\n", destValue)
		dest = curr.findNext(destValue)
		dest.insert(three)
		curr = curr.next
	}
	fmt.Printf("\n-- final (%d moves) --\n", moves)
	cups.print(curr.value)

	one := cups.findNext(1)
	fmt.Printf("final order: ")
	one.print(1)
	return one.toString("")
}

func play_game2(labels []int, size int, moves int) int {
	var cups, curr, three, dest *LinkedList
	var destValue int

	cups = buildRing(labels, size)
	if actualSize := cups.size(); actualSize != size {
		fmt.Printf("Ring size is %d (expected %d)", actualSize, size)
		os.Exit(1)
	}
	fmt.Printf("play_game: %d cups, %d moves\n", size, moves)
	curr = cups
	curr.printSubset(curr.value)

	node := make(map[int]*LinkedList)
	node[curr.value] = curr
	p := curr.next
	for p != curr {
		node[p.value] = p
		p = p.next
	}
	// fmt.Printf("[all %d nodes mapped]", size)

	for move := 0; move < moves; move++ {
		// fmt.Printf("\n-- move %d --\n", move+1)
		// curr.printSubset(curr.value)
		three = curr.cut(3)
		// fmt.Printf("pick up ")
		// three.print(0)

		if curr.value > 1 {
			destValue = curr.value - 1
		} else {
			destValue = size
		}
		for destValue == three.value || destValue == three.next.value ||
			destValue == three.next.next.value {
			if destValue > 1 {
				destValue = destValue - 1
			} else {
				destValue = size
			}
		}
		// fmt.Printf("destination: %d\n", destValue)
		dest = node[destValue]
		// dest.printSubset(0)

		dest.insert(three)
		curr = curr.next
	}
	fmt.Printf("\n-- final (%d moves) --\n", moves)
	curr.printSubset(curr.value)

	one := node[1]
	fmt.Printf("final: ")
	one.printSubset(1)
	return one.next.value * one.next.next.value

	return 0
}

func main() {
	fmt.Println("AoC 2020 - Day 23")
	fmt.Println("=================")

	fmt.Println("Example 1")
	cups := buildRing(exampleLabels, 0)
	size := cups.size()
	fmt.Printf("%d cups\n", size)

	var move int
	curr := cups
	for move = 0; move < 100; move++ {
		// fmt.Printf("\n-- move %d --\n", move+1)
		// cups.print(curr.value)
		curr = curr.play_move(size)
	}
	fmt.Printf("\n-- final (%d moves) --\n", move)
	cups.print(curr.value)

	one := cups.findNext(1)
	fmt.Printf("final order: ")
	one.print(1)

	fmt.Println("\nPart 1")
	cups = buildRing(inputLabels, 0)
	size = cups.size()
	fmt.Printf("%d cups\n", size)

	curr = cups
	for move = 0; move < 100; move++ {
		// fmt.Printf("\n-- move %d --\n", move+1)
		// cups.print(curr.value)
		curr = curr.play_move(size)
	}
	fmt.Printf("\n-- final (%d moves) --\n", move)
	cups.print(curr.value)

	one = cups.findNext(1)
	fmt.Printf("final order: ")
	one.print(1)

	fmt.Println("\nExample 1")
	result := play_game(exampleLabels, 100)
	fmt.Printf("result is %s\n", result)

	fmt.Println("\nPart 1")
	result = play_game(inputLabels, 100)
	fmt.Printf("result is %s\n", result)

	fmt.Println("\nExample 2")
	starProduct := play_game2(exampleLabels, 1000000, 10000000)
	fmt.Printf("result is %d\n", starProduct)

	fmt.Println("\nPart 2")
	starProduct = play_game2(inputLabels, 1000000, 10000000)
	fmt.Printf("result is %d\n", starProduct)

}
