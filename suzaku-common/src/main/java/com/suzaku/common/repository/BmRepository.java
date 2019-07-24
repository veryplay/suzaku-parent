package com.suzaku.common.repository;

import com.suzaku.common.entity.BmEntity;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface BmRepository extends CrudRepository<BmEntity, Long> {

    @Query("select u from BmEntity u where u.sn = :sn and u.isDel = 0")
    BmEntity getBySn(String sn);

}
