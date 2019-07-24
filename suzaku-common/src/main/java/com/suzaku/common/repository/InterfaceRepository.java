package com.suzaku.common.repository;

import com.suzaku.common.entity.InterfaceEntity;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface InterfaceRepository extends CrudRepository<InterfaceEntity, Long> {

    @Query("select u from InterfaceEntity u where u.sn = :sn and u.isDel = 0")
    List<InterfaceEntity> getBySn(String sn);
}
