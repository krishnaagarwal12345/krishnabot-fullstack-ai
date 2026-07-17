package com.krishna.ai_client.Controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.krishna.ai_client.Service.AiService;
import com.krishna.ai_client.model.AiRequest;
import com.krishna.ai_client.model.AiResponse;
import com.krishna.ai_client.model.RagRequest;
import com.krishna.ai_client.model.RagResponse;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class AiController {

   @Autowired
   private AiService aiService;

    // Home endpoint
    @GetMapping("/")
    public ResponseEntity<String> home() {
        return ResponseEntity.ok(
            "Spring Boot AI Client Running! 🚀"
        );
    }

    // Health check — checks Python API
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        String pythonHealth = aiService.healthCheck();
        return ResponseEntity.ok(
            "Spring Boot: OK | Python API: " + pythonHealth
        );
    }

    // Simple chat endpoint
    @PostMapping("/chat")
    public ResponseEntity<AiResponse> chat(
            @RequestBody AiRequest request) {

        AiResponse response = aiService.chat(
            request.getMessage()
        );
        return ResponseEntity.ok(response);
    }

    // Chat with custom system prompt
    @PostMapping("/chat/custom")
    public ResponseEntity<AiResponse> chatCustom(
            @RequestBody AiRequest request) {

        AiResponse response = aiService.chatWithPrompt(
            request.getMessage(),
            request.getSystemPrompt()
        );
        return ResponseEntity.ok(response);
    }

    // RAG query endpoint
    @PostMapping("/rag")
    public ResponseEntity<RagResponse> ragQuery(
            @RequestBody RagRequest request) {

        RagResponse response = aiService.ragQuery(
            request.getQuestion()
        );
        return ResponseEntity.ok(response);
    }

    // Quick test endpoint — no request body needed
    @GetMapping("/test")
    public ResponseEntity<AiResponse> test() {
        AiResponse response = aiService.chat(
            "Say hello in one sentence!"
        );
        return ResponseEntity.ok(response);
    }
}