package com.suzaku.common.service;

import com.suzaku.common.domian.Command;
import com.suzaku.common.entity.CommandEntity;
import com.suzaku.common.repository.CommandRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CommandService {

    @Autowired
    private CommandRepository commandRepository;

    private Command save(Command command) {

        CommandEntity commandEntity = new CommandEntity();
        commandEntity = commandRepository.save(commandEntity);

        return Command.builder().build();
    }

}
