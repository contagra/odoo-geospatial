/** @odoo-module */

/**
 * Copyright 2023 ACSONE SA/NV
 */

import {Layout} from "@web/search/layout";
import {useModel} from "@web/views/model";
import {usePager} from "@web/search/pager_hook";
import {useService} from "@web/core/utils/hooks";

const {Component, useState} = owl;

export class GeoengineController extends Component {
    /**
     * Setup the controller by using the useModel hook.
     */
    setup() {
        this.state = useState({isSavedOrDiscarded: false});
        this.actionService = useService("action");
        this.view = useService("view");
        this.editable = this.props.archInfo.editable;
        this.model = useModel(this.props.Model, {
            activeFields: this.props.archInfo.activeFields,
            resModel: this.props.resModel,
            fields: this.props.fields,
            limit: this.props.limit,
        });

        /**
         * Allow you to display records on the map thanks to the paging located
         * at the top right of the screen.
         */
        usePager(() => {
            const list = this.model.root;
            const {count, limit, offset} = list;
            return {
                offset: offset,
                limit: limit,
                total: count,
                onUpdate: async ({offset, limit}) => {
                    await list.load({limit, offset});
                    this.render(true);
                },
            };
        });
    }
    /** 0
     * Allow you to open the form editing view for the filled-in model.
     * @param {*} resModel
     * @param {*} resId
     */
    async openRecord(resModel, resId) {
        const {views} = await this.view.loadViews({resModel, views: [[false, "form"]]});
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            views: [[views.form.id, "form"]],
            res_id: resId,
            target: "new",
            context: {edit: false, create: false},
        });
    }

    async createRecord(resModel, field, value) {
        const {views} = await this.view.loadViews({resModel, views: [[false, "form"]]});
        const context = {};
        context[`default_${field}`] = value;
        this.actionService.doAction(
            {
                type: "ir.actions.act_window",
                res_model: resModel,
                views: [[views.form.id, "form"]],
                target: "new",
                context,
            },
            {
                onClose: async () => await this.onSaveRecord(),
            }
        );
    }

    async onSaveRecord() {
        const offset = this.model.root.count + 1;
        await this.model.root.load({limit: 80, offset});
        this.render(true);
    }

    async onClickSave() {
        this.state.isSavedOrDiscarded = true;
        await this.model.root.editedRecord.save();
    }

    async onClickDiscard() {
        this.state.isSavedOrDiscarded = true;
        await this.model.root.editedRecord.discard();
    }

    async updateRecord(value) {
        this.state.isSavedOrDiscarded = false;
        const newValue = {};
        const key = Object.keys(this.model.root.fields).find(
            (el) => this.model.root.fields[el].geo_type !== undefined
        );
        newValue[key] = value;
        await this.model.root.editedRecord.update(newValue);
    }
}

GeoengineController.template = "base_geoengine.GeoengineController";
GeoengineController.components = {Layout};
