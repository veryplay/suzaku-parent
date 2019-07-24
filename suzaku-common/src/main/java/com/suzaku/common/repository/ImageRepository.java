package com.suzaku.common.repository;

import com.suzaku.common.entity.ImageEntity;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface ImageRepository extends CrudRepository<ImageEntity, Integer> {


}
