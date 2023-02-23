/** @odoo-module */
import {Layout} from "@web/search/layout";
import {useModel} from "@web/views/model";
import {usePager} from "@web/search/pager_hook";

const {Component} = owl;

export class GeoengineController extends Component {
    setup() {
        this.model = useModel(this.props.Model, {
            resModel: this.props.resModel,
            fields: this.props.fields,
            limit: this.props.limit,
        });

        usePager(() => {
            const list = this.model.root;
            const {count, lim, off} = list;
            return {
                offset: off,
                limit: lim,
                total: count,
                onUpdate: async ({offset, limit}) => {
                    await list.load({limit, offset});
                    this.render(true);
                },
            };
        });
    }
}

GeoengineController.template = "base_geoengine.GeoengineController";
GeoengineController.components = {Layout};