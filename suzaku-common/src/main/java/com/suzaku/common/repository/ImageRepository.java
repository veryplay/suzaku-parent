package com.suzaku.common.repository;

import com.suzaku.common.entity.ImageEntity;
import org.springframework.data.repository.CrudRepository;

public interface ImageRepository extends CrudRepository<ImageEntity, Integer> {
}
