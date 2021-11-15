package main

import (
	"testing"
)

func TestBuildRing(t *testing.T) {
	cups := buildRing(exampleLabels, 0)
	if cups.next == nil || cups.prev == nil {
		t.Fatalf("Not a double-linked ring")
	}
	p := cups.next
	for p != cups {
		if p.next == nil || p.prev == nil {
			t.Fatalf("Links missing")
		}
		p = p.next
	}
}

