package com.krishna.ai_client.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;
@Data
public class AiResponse {
    @JsonProperty("response")
     private String response;

     @JsonProperty("model")
     private String model;
     

    
    @JsonProperty("chunks")
    private  List<String> relevantChunks;
    

    
}
