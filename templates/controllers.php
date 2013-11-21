<?php

class [[controller_name]]Controller extends [[extend_from]]_SiteController
{
    protected function configure()
    {
        $this->useTemplate('[[view_path]]');
        $this->data['pouet_array'] = r()->getIterator();
    }
}
