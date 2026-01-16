package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
)

type Config struct {
	FormatType string `json:"formatType"`
}

func main() {
	// 1. Read config/settings.json
	// The prompt example says `../config/settings.json` relative to parser.go
	configPath := filepath.Join("..", "config", "settings.json")
	configFile, err := os.ReadFile(configPath)
	if err != nil {
		fmt.Printf("Error reading config file at %s: %v\n", configPath, err)
		os.Exit(1)
	}

	var config Config
	if err := json.Unmarshal(configFile, &config); err != nil {
		fmt.Printf("Error parsing config file: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Config loaded: formatType=%s\n", config.FormatType)

	// 2. Read utils/format.ts
	// The prompt example says `utils/format.ts` relative to parser.go
	formatPath := filepath.Join("utils", "format.ts")
	formatFile, err := os.ReadFile(formatPath)
	if err != nil {
		fmt.Printf("Error reading format file at %s: %v\n", formatPath, err)
		os.Exit(1)
	}

	formatContent := string(formatFile)

	// 3. Parse the TS file to find the config
	// We are looking for something like:
	// key: {
	//   delimiter: "val",
	//   hasHeader: bool
	// }

	// This regex looks for the key followed by colon and opening brace
	// It's a simple heuristic parser
	pattern := fmt.Sprintf(`%s\s*:\s*\{([^}]+)\}`, regexp.QuoteMeta(config.FormatType))
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(formatContent)

	if len(matches) < 2 {
		fmt.Printf("Error: Format definition for '%s' not found in %s\n", config.FormatType, formatPath)
		// This simulates the "bug" being traced to format.ts if the key is missing
		os.Exit(1)
	}

	definition := matches[1]

	// Parse the definition body (delimiter and hasHeader)
	// Naive parsing for demonstration
	delimiterRe := regexp.MustCompile(`delimiter\s*:\s*["']([^"']+)["']`)
	headerRe := regexp.MustCompile(`hasHeader\s*:\s*(true|false)`)

	delimiterMatch := delimiterRe.FindStringSubmatch(definition)
	headerMatch := headerRe.FindStringSubmatch(definition)

	delimiter := "unknown"
	if len(delimiterMatch) >= 2 {
		delimiter = delimiterMatch[1]
	}

	hasHeader := "unknown"
	if len(headerMatch) >= 2 {
		hasHeader = headerMatch[1]
	}

	fmt.Printf("Found format definition for '%s':\n", config.FormatType)
	fmt.Printf("  Delimiter: %s\n", delimiter)
	fmt.Printf("  Has Header: %s\n", hasHeader)
}
