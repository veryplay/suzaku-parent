package com.suzaku.common.repository;

import com.suzaku.common.entity.CommandEntity;
import org.springframework.data.repository.CrudRepository;

public interface CommandRepository extends CrudRepository<CommandEntity, Long> {
}
