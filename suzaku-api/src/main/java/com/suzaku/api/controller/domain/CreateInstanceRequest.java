package com.suzaku.api.controller.domain;

import lombok.Data;

import javax.validation.constraints.NotBlank;

@Data
public class CreateInstanceRequest {

    @NotBlank
    private String instanceType;

    @NotBlank
    private String imageId;


}
